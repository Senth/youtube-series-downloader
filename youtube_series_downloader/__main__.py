import argparse
from youtube_series_downloader.logger import log_message
from youtube_series_downloader.downloader import Downloader
from .channel import Channel
from .config import config

def __main__():
    args = _get_args()
    config.add_args_settings(args)

    total_downloaded = 0
    channels = Channel.create_from_config()
    for channel in channels:
        videos = channel.get_videos()
        log_message('') # Just some padding

        for video in videos:
            downloader = Downloader(channel, video)

            if not downloader.has_downloaded():
                downloader.download()
                total_downloaded += 1
            else:
                log_message('------ Skipping {}, no new videos to download ------'.format(channel.name))

    log_message('\n\n\nDownloaded {} episodes'.format(total_downloaded))


def _get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Prints out helpful messages.')
    parser.add_argument('-p', '--pretend', action='store_true',
                        help='Only pretend to download, convert, and store files.')
    parser.add_argument('-t', '--threads', type=int,
                        help='Override the config settings with how many threads you want to use')
    parser.add_argument('-d', '--daemon', action='store_true',
                        help='Run the script as a daemon instead of once')
    parser.add_argument('--max-days-back', type=int, default=3,
                        help='How many days back we should check for videos')

    return parser.parse_args()
