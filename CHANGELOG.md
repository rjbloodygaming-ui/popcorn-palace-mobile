# Changelog

Changes in Popcorn Palace Mobile, newest first. The same history is available offline in the app under **Settings → Changelog** or **Menu → Changelog**.

## 0.6.19-beta — 2026-10-28

### Changed

- Watch History now contains only episodes marked watched. Unwatched episodes appear in Continue Watching; Finished Episodes remains watched-only.
- Marking an episode watched or unwatched moves it between the appropriate views while preserving its resume position, saved history, seasons and numeric episode order.

## 0.6.18-beta — 2026-10-28

### Added

- Saved episode metadata retains season, episode number and source order so editing an episode title does not change its place in history. Older records use the season/episode information already present in their titles and URLs.

### Changed

- Tapping Next episode now marks the episode being left as watched before opening the next episode. Resume positions and actual watch time are preserved.
- Saved episodes inside Watch History are grouped into seasons and sorted numerically, such as 1, 2, 3 and 10, instead of by last-viewed time. The same saved-season layout is used in Finished Episodes and Continue Watching.

## 0.6.17-beta — 2026-10-25

### Added

- Added Category info on title pages, with a copyable diagnostic summary of the extracted genres, countries and category.
- Added an all-category search action when titles could not be classified.

### Fixed

- Scoped searches now check title-page category, genre and production-country metadata, including structured data, to identify untagged anime without requiring a matching dubbed/subbed listing.
- Titles with unverified categories are withheld from restricted searches instead of being assumed to be normal Movies/TV results. Discover continues to include them.

### Changed

- Category lookups are cached and run in parallel with a 25-second overall wait limit. Animation with Japanese origin is classified as Anime; other animation is not automatically treated as anime.

## 0.6.16-beta — 2026-10-25

### Fixed

- Unmarked alternate listings of a known anime title are now classified as Anime before search filtering, including listings without a DUB/SUB prefix.
- Recognized anime classification is retained across app restarts so an unmarked version stays out of general Movies/TV searches when it appears alone later.

### Changed

- Alternate-title matching requires the normalized full title and movie/series format, supported by a matching release year or cover image. Conflicting years are rejected, and no language/edition is guessed.

## 0.6.15-beta — 2026-10-25

### Fixed

- Anime films no longer appear in general Movies searches, and anime series no longer appear in general TV Shows searches. Anime remains searchable in its own categories and in Discover.
- Selecting an anime or Movies/TV category link clears an incompatible previous media-type filter.

### Changed

- Non-anime animated movies remain in Movies; anime search still respects the selected dubbed/subbed and movie/series category.

## 0.6.14-beta — 2026-10-25

### Added

- Search now stays within the active sidebar catalogue, including Movies, TV Shows, anime selections and Audiobooks. Searching from Discover includes all categories.
- Search headings and input hints show the active scope. Clearing a search returns to the same catalogue.

### Fixed

- Audiobook searches now submit the entered query instead of reloading the audiobook browse page.
- Search results are filtered using returned or previously saved content metadata before any catalogue-context labels are applied.

## 0.6.13-beta — 2026-10-25

### Added

- Added current-show or audiobook artwork to the playback notification and media session, enabling artwork backgrounds on supported Android/One UI media controls.
- Uses the title banner when available, with the show or book cover as fallback.

### Changed

- Artwork loads in the background without delaying playback and stays with the playback service while the app is minimized or the phone is locked.
- Switching titles clears old artwork; late image responses are ignored after a source change or Stop. Existing playback controls are retained.

## 0.6.12-beta — 2026-10-25

### Added

- Added Remove on Continue Watching show cards and inside each saved show. Removal hides the show from that list while keeping watch history, watched status and resume positions.
- Added Undo removal for the last removed show. Starting an episode from a hidden show again also restores it to Continue Watching.

### Fixed

- Missing or failed show covers in Watch History, Finished Episodes and Continue Watching now trigger a background lookup on the title page. Recovered cover links are saved for future visits.
- Expanded title-page cover parsing to handle alternate image metadata and lazy poster elements.

### Changed

- Continue Watching removals persist on this device when the app is reopened.

## 0.6.11-beta — 2026-10-25

### Fixed

- Finished Episodes, Watch History and Continue Watching now group saved episodes by show instead of displaying a flat episode list.

### Changed

- Show cards use the same responsive poster grid as search results. Tap a card to view that show’s saved episodes, resume positions and watched controls.
- Show titles and covers are saved with new history entries. Older history uses saved show information or a recognizable title URL when available.

## 0.6.10-beta — 2026-10-25

### Added

- Added an offline Changelog in Settings and the navigation menu, with version numbers, dates and grouped changes.
- Included release history back to 0.6.4 so users can review earlier fixes.

### Changed

- GitHub release notes now list Added, Fixed and Changed items and link to the full changelog.
- The publisher checks that release notes, the GitHub changelog and the app's bundled history match before publishing.

## 0.6.9-beta — 2026-10-25

### Fixed

- Removed the duplicate AnimeDubSerie option that returned an empty listing.
- Redirected the old dubbed-series category to AnimeDubSeries.

### Changed

- Renamed anime categories to clear Dubbed/Subbed movies/series labels.

## 0.6.8-beta — 2026-10-24

### Fixed

- Playback now pauses when leaving Player for the episode list, Discover, Favorites or history.
- Leaving the Player screen while a source is preparing also prevents it from starting later.

### Changed

- Saved playback positions are retained; minimizing or locking the phone from Player still allows background playback.

## 0.6.7-beta — 2026-10-24

### Changed

- Replaced the app icon with the supplied popcorn artwork.
- Added proportional icon scaling, adaptive launcher shapes, safe padding and themed-icon support.

## 0.6.6-beta — 2026-10-24

### Changed

- Version-only update from 0.6.5 to test in-app updating. No feature or behavior changes.

## 0.6.5-beta — 2026-10-24

### Added

- Added GitHub update checks whenever the app opens or returns to the foreground.
- Added Settings controls for manual checks, automatic checks, Update, Later and Skip this version.
- Added background APK downloads and verification of checksum, package, version and signing certificate before installation.

## 0.6.4-beta — 2026-10-24

### Changed

- Kept the video decoder output alive in the playback service while the app is minimized or locked.
- Returning to Player reconnects the visible video window without recreating the decoder output, targeting interruptions on app return.
