# youtube-series-downloader

[![Latest PyPI version](https://img.shields.io/pypi/v/youtube-series-downloader.svg)](https://pypi.python.org/pypi/youtube-series-downloader)

Downloads new YouTube episodes from configurable channels and adds them in a [plex](https://plex.tv/) friendly format.

## Features

- Download latest episodes from configurable channels. Configurable how many days back to look for an episode.
- Speed up videos. Configurable both globally and separate for each channel.
- Run as a daemon.
- Plex friendly output.
- Include/exclude regex filters to only download episodes matching the title.

## Usage

```
usage: youtube-series-downloader [-h] [-v] [-p] [-t THREADS] [-d] [--max-days-back MAX_DAYS_BACK] [--debug]

optional arguments:
  -d, --daemon    Run the script as a daemon instead of once
  -p, --pretend   Only pretend to download, convert, and store files

  -t THREADS, --threads THREADS
                  Override the config settings with how many threads you want to use
  --max-days-back MAX_DAYS_BACK
                  How many days back we should check for videos

  -h, --help      show this help message and exit
  -v, --verbose   Prints out helpful messages
  --debug         Turn on debug messages. This automatically turns on --verbose as well.
```

## Installation

Run the commands below and follow the instructions.

```
$ pip install --user youtube-series-downloader
$ youtube-series-downloader
```

### Requirements

- ffmpeg to be installed and available through the PATH environmental variable.
- youtube-dl available through the PATH environmental variable.

## Licence

MIT

## Authors

`youtube-series-downloader` was written by `Matteus Magnusson <senth.wallace@gmail.com>`.
