# youtube-series-downloader

[![Latest PyPI version](https://img.shields.io/pypi/v/youtube-series-downloader.svg)](https://pypi.python.org/pypi/youtube-series-downloader)

Downloads new YouTube episodes from configurable channels and adds them in a [plex](https://plex.tv/) friendly format.

## Features

- Download latest episodes from configurable channels. Configurable how many days.
- Speed up videos. Both globally configurable and each channel can override the speed.
- Run as a daemon.
- Plex friendly output
- Include/exclude regex filters to only download episodes matching the title

## Usage

```
$ youtube-series-downloader --help
```

## Installation

Run the command below and follow the instructions

```
$ pip install --user youtube-series-downloader && youtube-series-downloader
```

### Requirements

- ffmpeg to be installed and available through the PATH environmental variable
- youtube-dl available through the PATH environmental variable

## Licence

MIT

## Authors

`youtube-series-downloader` was written by `Matteus Magnusson <senth.wallace@gmail.com>`.
