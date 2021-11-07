# youtube-series-downloader

[![python](https://img.shields.io/pypi/pyversions/youtube-series-downloader.svg)](https://pypi.python.org/pypi/youtube-series-downloader)
[![Latest PyPI version](https://img.shields.io/pypi/v/youtube-series-downloader.svg)](https://pypi.python.org/pypi/youtube-series-downloader)
[![Downloads](https://pepy.tech/badge/youtube-series-downloader)](https://pepy.tech/project/youtube-series-downloader?right_color=orange)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/Senth/youtube-series-downloader.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/Senth/youtube-series-downloader/alerts/)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/Senth/youtube-series-downloader.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/Senth/youtube-series-downloader/context:python)

Downloads new YouTube episodes from configurable channels and adds them in a [plex](https://plex.tv/) friendly format.

## Features

- Download latest episodes from configurable channels. Configurable how many days back to look for an episode.
- Speed up videos. Configurable both globally and separate for each channel.
- Run as a daemon.
- Plex friendly output.
- Include/exclude regex filters to only download episodes matching the title.

## Usage

```usage
usage: youtube-series-downloader [-h] [-v] [-p] [-t THREADS] [-d] [--max-days-back MAX_DAYS_BACK] [--debug]

optional arguments:
  -d, --daemon    Run the script as a daemon instead of once.
  -p, --pretend   Only pretend to download, convert, and store files.

  -t THREADS, --threads THREADS
                  How many threads you want to use (overrides config file).
  --max-days-back MAX_DAYS_BACK
                  How many days back we should check for videos (overrides config file).

  -h, --help      show this help message and exit.
  -v, --verbose   Prints out helpful messages.
  -s, --silent    Turn off all messages except errors.
  --debug         Turn on debug messages. This automatically turns on --verbose as well.
```

## Installation

Run the commands below and follow the instructions.

```properties
pip install --user --upgrade youtube-series-downloader
youtube-series-downloader
```

### Requirements

- ffmpeg to be installed and available through the PATH environmental variable.

## Authors

`youtube-series-downloader` was written by `Matteus Magnusson <senth.wallace@gmail.com>`.
