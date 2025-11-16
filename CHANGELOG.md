# Changelog

All notable changes to this project will be documented in this file

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.6.0] - 2025-11-16

### Added

- Ability to pass in a custom cookies file through the configuration file with `cookies_file = /path/to/cookies.txt`.

## [1.5.1] - 2021-11-13

### Fixed

- Logging indentation is not reset when an exception is thrown [#33](https://github.com/Senth/youtube-series-downloader/issues/33)
- Changed from `youtube-dl` to `yt-dlp` to once again download videos in full speed [#32](https://github.com/Senth/youtube-series-downloader/issues/32)

## [1.5.0] - 2021-11-04

### Added

- Ability to change `log_level` through the config file

## [1.4.1] - 2021-11-04

### Changed

- Updated dependency of tealprint `0.1.0` -> `0.2.1`

## [1.4.0] - 2021-07-23

### Added

- Multiple channels can now have the same name and use a common episode counter [#25](https://github.com/Senth/youtube-series-downloader/issues/25)
  - This is useful when a content creator has multiple channels but you want to put them
    into the same series.
- Quits application if configuration is missing required settings
  - `series_dir = /media/series` under `[General]`
  - `id = youtube_channel_id` under `[Channel Name]`

### Fixed

- If quitting the application in the middle of a render ffmpeg would get stuck next time
  since you had to confirm the replacement of the file

## [1.3.4] - 2021-07-22

### Fixed

- Default speed is now read correctly

## [1.3.3] - 2021-07-21

### Fixed

- Misspelled `merge_output_format` with an additional 's' at the end, didn't merge correctly into an `mkv` file.

## [1.3.2] - 2021-07-21

### Fixed

- Can now use `[vars]` in configuration

## [1.3.1] - 2021-07-21

### Fixed

- Used `youtube_dl` wrongly which made the application unusable

## [1.3.0] - 2021-07-20

### Breaking Changes

- Configuration is now stored as an cfg-file instead of py, and in your home directory [#16](https://github.com/Senth/youtube-series-downloader/issues/16)
  - Unfortunately, you'll have to move everything to the new configuration file.

### Added

- In `--daemon` mode, the configuration is re-read before every check.
  Meaning that you don't have to restart the daemon when the configuration changes.
- Some tests [#17](https://github.com/Senth/youtube-series-downloader/issues/17)

### Changed

- Now calls `youtube-dl` from the python package instead of through CLI [#18](https://github.com/Senth/youtube-series-downloader/issues/18).
  This means you don't have to have `youtube-dl` in your `PATH` environment anymore.
- Improved `--verbose` logging to be more complete in why a video was filtered out or passed the filters

### Fixed

- Exclude pattern now actually excludes videos [#15](https://github.com/Senth/youtube-series-downloader/issues/15)

## [1.2.1] - 2021-04-05

### Fixed

- Added missing `--silent` in README

## [1.2.0] - 2021-04-05

### Added

- `--silent -s` flag to turn off all messages

### Changed

- Improve wording in help/readme
- Improve logging with emojis, colors and indent
- More logging by default (turn off all by using `--silent`)

### Removed

- System wide configuration (user configuration is still available)

### Fixed

- Now downloads oldest episodes first (so they come in the correct order) [#10](https://github.com/Senth/youtube-series-downloader/issues/10)
- Exits the program if you don't have

## [1.1.8] - 2021-04-04

### Fixed

- `config.example.py` updated so that you can use include and exclude at the same time

## [1.1.7] - 2020-11-20

### Changed

- Now downloads the best format.

### Fixed

- Didn't work for videos that were below 1080p or didn't have 60fps.

## [1.1.6] - 2020-11-20

### Fixed

- Crash when using --verbose or --debug when trying to download or convert a file.

## [1.1.5] - 2020-11-20

### Changed

- Improve "Skipping CHANNEL_NAME, no new videos to download" to be precise.

### Fixed

- Regex issue with video title. It worked anyway, but better to fix it.

## [1.1.4] - 2020-11-20

### Fixed

- Bug where the config didn't check the CHANNEL for correct syntax

## [1.1.3] - 2020-11-??

Before started using changelog
