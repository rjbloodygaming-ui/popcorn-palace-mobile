"""Publish an already signed APK. No signing credentials or application source belong here."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

REPO = "rjbloodygaming-ui/popcorn-palace-mobile"
SIGNER = "37a02dbd9857bf8a077a45f61a0efdeb9932bcdaaca78538f1cd0ecfaddef391"


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
    tools = os.environ.get("ANDROID_BUILD_TOOLS")
    if not tools:
        sdk = Path(os.environ.get("ANDROID_HOME", os.environ.get("ANDROID_SDK_ROOT", "/usr/local/lib/android/sdk")))
        candidates = [p for p in (sdk / "build-tools").glob("*") if (p / "apksigner").is_file()]
        if not candidates:
            raise RuntimeError("Android build tools are required to verify the signed APK")
        tools = max(candidates, key=lambda p: [int(n) for n in re.findall(r"\d+", p.name)])
    tools = Path(tools)
    cert = subprocess.check_output([str(tools / "apksigner"), "verify", "--print-certs", str(apk)], text=True)
    signers = {digest.lower().replace(":", "") for digest in re.findall(r"Signer #\d+(?: \([^\n]*?\))? certificate SHA-256 digest:\s*([a-fA-F0-9:]+)", cert)}
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
        notes.write_text(data["notes"] + "\n\nInstall over the existing app; do not uninstall first.\n")
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
