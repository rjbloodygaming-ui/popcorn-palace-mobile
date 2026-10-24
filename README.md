# Popcorn Palace Mobile updates

Official update repository for this personal Android app. Download the newest signed APK from [Releases](https://github.com/rjbloodygaming-ui/popcorn-palace-mobile/releases/latest).

Install over your current version to keep favorites, history and settings. Do not uninstall first. Install version 0.6.5 once manually to enable future in-app updates.

The app checks GitHub whenever it opens or returns to the foreground. Settings includes **Check for updates** and an automatic-check toggle. New versions offer Update, Later and Skip this version. Downloads continue through Android's download service; return to the app to verify and install them. Android may request **Allow from this source** and an installation confirmation.

APK size, SHA-256, package ID, increasing Android version code and the existing app signing certificate are checked before installation. Update checks require no GitHub login. An active playback session defers automatic update prompts.

## Publishing the next update

1. Build and sign the APK privately using the original signing key and a higher `versionCode`.
2. Put the signed APK in the repository root with the same filename pattern as the existing build.
3. Update `release-input.json` with its version, path, byte size, SHA-256 and release notes.
4. Commit those changes to `main` together. The publishing workflow verifies the APK and publishes a GitHub Release containing the APK and `update.json`. An unchanged release can be safely retried; conflicting existing versions are rejected.

Only signed release binaries, public metadata and publishing tools belong in this repository. Application source, keystores, signing passwords and access tokens must remain private. GitHub Actions uses its built-in repository token to publish releases.

This independent app is not affiliated with GitHub, NEPU, Popcorn Palace or VRChat.
