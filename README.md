# Popcorn Palace Mobile

Popcorn Palace Mobile is an independent Android app for browsing NEPU's catalogue and streaming movies, TV shows, anime and audiobooks. It brings discovery, playback, favorites and watch history together in a native Android interface, with background audio and built-in app updates.

**[Download the latest Android APK](https://github.com/rjbloodygaming-ui/popcorn-palace-mobile/releases/latest)**

## Changelog

Read the [full changelog](CHANGELOG.md) for fixes and features in each release. Inside the app, open **Settings → Changelog** or **Menu → Changelog**; installed release history is available offline. New GitHub releases also include a list of what was added, fixed or changed.

## Features

### Browse and discover

- Search for titles and explore a poster-based catalogue.
- Browse movies, TV shows, anime and audiobooks through categories and filters.
- Choose dubbed or subbed anime, with separate movie and series categories.
- Browse episode lists by season, with your selected season remembered.
- Sort results by newest, popular, release date or IMDb where supported by the source.

### Watch and listen

- Stream supported video and audio sources with native Android playback, including HLS.
- Use full-screen video, seek through playback, and skip backward or forward by 10 seconds.
- Move to the next episode from the player when another episode is available.
- Keep audio playing while the app is minimized or your phone is locked.
- Control playback from notifications and the lock screen, including play, pause, seeking and Stop. Available controls and their layout depend on Android and your device.
- Use supported headset and Bluetooth media controls.

Returning from Player to the episode list, Discover or another screen inside the app pauses playback and keeps your position. Minimizing the app or locking your phone while on Player allows playback to continue in the background. Returning to a paused session leaves it paused until you press Play.

### Organize your library

- Save favorites and organize them into multiple custom categories.
- Browse Finished Episodes, Watch History and Continue Watching by show, using the same poster grid as search.
- Tap a show to see its saved episodes, resume positions and watched controls.
- Remove a show from Continue Watching without deleting history or progress; undo the last removal or start an episode again to restore it.
- Resume saved episodes and audiobooks from their last recorded position.
- Track approximate playback time and automatically mark episodes watched near completion.
- Manually mark episodes watched or unwatched and edit saved episode titles.
- Export and import favorites, custom categories and watch history as a backup.

Favorites, history, settings and saved positions are stored on your device. Updates installed over the existing app preserve this data.

### Built-in updates

- Check for new app versions whenever the app opens or returns to the foreground.
- Check manually through **Settings → Check for updates**.
- Choose **Update**, **Later** or **Skip this version**, or turn automatic checks off.
- Download app updates through Android's download service, then return to the app to install.
- Verify the downloaded update's checksum, package, version and signing certificate before opening Android's installer.

Updates are distributed through GitHub Releases. A GitHub account is not required to check for or download updates. Automatic update prompts are deferred while a playback session is active.

## Installation

1. Open the [latest release](https://github.com/rjbloodygaming-ui/popcorn-palace-mobile/releases/latest).
2. Download the file ending in **`.apk`** under **Assets**.
3. Open it on your Android device and follow the installation prompts. Android may ask you to allow installation from the app you used to open the APK.

For future updates, use the app's updater or install a newer APK over the existing version. **Do not uninstall first** if you want to keep your saved data. The in-app updater may ask you to enable **Allow from this source** for Popcorn Palace Mobile, followed by Android's installation confirmation.

## Requirements and current limits

- **Android 8.0 or newer** and an internet connection.
- Catalogue and stream availability depend on NEPU and the media formats supported by your device.
- Site verification, when required, opens a visible verification screen in the app.
- Playback is streaming-only; offline media downloads and subtitles are not currently supported.
- The app is a beta, so behavior may vary between devices and media sources.

This repository hosts signed Android releases and update-publishing files. Application source and signing credentials are kept private.

Popcorn Palace Mobile is an independent project and is not affiliated with NEPU, Popcorn Palace or VRChat.
