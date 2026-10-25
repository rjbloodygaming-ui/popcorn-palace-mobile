"""Publish an already signed APK. No signing credentials or application source belong here."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
import zipfile

REPO = "rjbloodygaming-ui/popcorn-palace-mobile"
SIGNER = "37a02dbd9857bf8a077a45f61a0efdeb9932bcdaaca78538f1cd0ecfaddef391"
SECTIONS = ("Added", "Fixed", "Changed")


def parse_history(raw):
    releases = json.loads(raw)["releases"]
    if not isinstance(releases, list) or not releases:
        raise ValueError("A release changelog is required")
    codes = set()
    names = set()
    for entry in releases:
        code, name = entry["versionCode"], entry["versionName"]
        if type(code) is not int or code <= 0 or code in codes or name in names:
            raise ValueError("Invalid or duplicate changelog version")
        codes.add(code)
        names.add(name)
        if not re.fullmatch(r"\d+\.\d+\.\d+(?:-[A-Za-z0-9.]+)?", name) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", entry["date"]):
            raise ValueError("Invalid changelog version or date")
        count = 0
        for section in SECTIONS:
            lines = entry.get(section, [])
            if not isinstance(lines, list) or any(not isinstance(line, str) or not line.strip() or "\n" in line for line in lines):
                raise ValueError("Changes must be nonempty, single-line descriptions")
            count += len(lines)
        if not count:
            raise ValueError("Describe what was added, fixed or changed before publishing")
    return sorted(releases, key=lambda entry: entry["versionCode"], reverse=True)


def change_notes(entry, markdown=False, heading=2):
    sections = []
    for section in SECTIONS:
        if entry.get(section):
            title = "#" * heading + " " + section if markdown else section + ":"
            bullet = "- " if markdown else "• "
            sections.append(title + "\n\n" + "\n".join(bullet + line for line in entry[section]))
    return "\n\n".join(sections)


def render_history(releases):
    intro = "# Changelog\n\nChanges in Popcorn Palace Mobile, newest first. The same history is available offline in the app under **Settings → Changelog** or **Menu → Changelog**.\n\n"
    return intro + "\n\n".join("## " + entry["versionName"] + " — " + entry["date"] + "\n\n" + change_notes(entry, markdown=True, heading=3) for entry in releases) + "\n"


def prepare():
    data = json.loads(Path("release-input.json").read_text())
    name, code = data["versionName"], data["versionCode"]
    if not re.fullmatch(r"\d+\.\d+\.\d+(?:-[A-Za-z0-9.]+)?", name) or type(code) is not int or code <= 0:
        raise ValueError("Invalid release version")
    filename = f"Popcorn-Palace-Mobile-{name}.apk"
    if data["packageName"] != "app.nepu.player" or data["apk"] != filename:
        raise ValueError("Unexpected package or APK path")
    apk = Path(data["apk"])
    digest = hashlib.sha256(apk.read_bytes()).hexdigest()
    if digest != data["sha256"] or apk.stat().st_size != data["size"]:
        raise ValueError("APK hash/size mismatch")
    releases = parse_history(Path("changelog.json").read_text(encoding="utf-8"))
    current = releases[0]
    if current["versionCode"] != code or current["versionName"] != name:
        raise ValueError("Add a changelog entry for the version being published")
    if data["notes"] != change_notes(current):
        raise ValueError("Update prompt notes must match the current changelog entry")
    if Path("CHANGELOG.md").read_text(encoding="utf-8") != render_history(releases):
        raise ValueError("Regenerate CHANGELOG.md from changelog.json")
    with zipfile.ZipFile(apk) as package:
        embedded = json.loads(package.read("assets/changelog.json"))
    if embedded != {"releases": releases}:
        raise ValueError("The app's offline changelog must match the published history")
    tools = os.environ.get("ANDROID_BUILD_TOOLS")
    if not tools:
        sdk = Path(os.environ.get("ANDROID_HOME", os.environ.get("ANDROID_SDK_ROOT", "/usr/local/lib/android/sdk")))
        candidates = [p for p in (sdk / "build-tools").glob("*") if (p / "apksigner").is_file()]
        if not candidates:
            raise RuntimeError("Android build tools are required to verify the signed APK")
        tools = max(candidates, key=lambda p: [int(n) for n in re.findall(r"\d+", p.name)])
    tools = Path(tools)
    cert = subprocess.check_output([str(tools / "apksigner"), "verify", "--print-certs", str(apk)], text=True)
    signers = {digest.lower().replace(":", "") for digest in re.findall(r"(?:Signer #\d+|V[0-9.]+ Signer:) certificate SHA-256 digest:\s*([a-fA-F0-9:]+)", cert)}
    if signers != {SIGNER}:
        print(cert)
        raise ValueError("APK does not use the original app signing certificate")
    badging = subprocess.check_output([str(tools / "aapt2"), "dump", "badging", str(apk)], text=True)
    package = re.search(r"package: name='([^']+)' versionCode='([^']+)' versionName='([^']+)'", badging)
    if not package or package.groups() != (data["packageName"], str(code), name):
        raise ValueError("APK package/version disagrees with release metadata")
    tag = "v" + name
    manifest = {k: data[k] for k in ("versionCode", "versionName", "packageName", "sha256", "size", "notes")}
    manifest["apkUrl"] = f"https://github.com/{REPO}/releases/download/{tag}/{filename}"
    return data, apk, tag, manifest


def main():
    data, apk, tag, manifest = prepare()
    if os.environ.get("VERIFY_ONLY") == "1":
        print("Verified APK signature, package, version, size and checksum.")
        return
    if os.environ.get("GH_REPO") != REPO:
        raise ValueError("Unexpected publishing repository")
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        update = tmp / "update.json"
        update.write_text(json.dumps(manifest, indent=2) + "\n")
        notes = tmp / "notes.md"
        current = parse_history(Path("changelog.json").read_text(encoding="utf-8"))[0]
        notes.write_text(change_notes(current, markdown=True) + "\n\n## Full changelog\n\n[View all changes](https://github.com/" + REPO + "/blob/main/CHANGELOG.md). In the app: **Settings → Changelog**.\n\nInstall over the existing app; do not uninstall first.\n", encoding="utf-8")
        exists = subprocess.run(["gh", "release", "view", tag], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0
        if exists:
            subprocess.run(["gh", "release", "download", tag, "--pattern", "update.json", "--pattern", apk.name, "--dir", str(tmp / "existing")], check=True)
            old = json.loads((tmp / "existing/update.json").read_text())
            old_hash = hashlib.sha256((tmp / "existing" / apk.name).read_bytes()).hexdigest()
            if old != manifest or old_hash != manifest["sha256"]:
                raise ValueError("An existing release differs. Publish a new version instead of replacing it.")
            print("Identical release already exists.")
            return
        # gh uploads both assets to a draft before publishing the complete release.
        command = ["gh", "release", "create", tag, str(apk), str(update), "--title", f"Popcorn Palace Mobile {data['versionName']}", "--notes-file", str(notes), "--latest"]
        if os.environ.get("GITHUB_SHA"):
            command += ["--target", os.environ["GITHUB_SHA"]]
        subprocess.run(command, check=True)


if __name__ == "__main__":
    main()
