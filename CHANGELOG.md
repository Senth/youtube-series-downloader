# Changelog

All notable changes to this project will be documented in this file

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
