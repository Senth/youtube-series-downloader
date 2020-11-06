from __future__ import annotations
from apscheduler.schedulers.blocking import BlockingScheduler
import logging
from .config import config
from .program_checker import check_for_programs
from .logger import log_message
from .downloader import Downloader
from .channel import Channel


def __main__():
    check_for_programs()

    # Set logger for apscheduler depending on verbosity
    if config.verbose:
        logging.getLogger("apscheduler").setLevel(logging.WARNING)
    else:
        logging.getLogger("apscheduler").setLevel(logging.ERROR)

    if config.daemon:
        _daemon()
    else:
        _run_once()


def _daemon():
    scheduler = BlockingScheduler()
    scheduler.add_job(_run_once, "interval", minutes=10, max_instances=1)
    scheduler.start()


def _run_once():
    total_downloaded = 0
    channels = Channel.create_from_config()
    for channel in channels:
        videos = channel.get_videos()
        log_message("")  # Just some padding

        for video in videos:
            downloader = Downloader(channel, video)

            if not downloader.has_downloaded():
                downloader.download()
                total_downloaded += 1
            else:
                log_message(
                    "------ Skipping {}, no new videos to download ------".format(
                        channel.name
                    )
                )

    log_message("\n\n\nDownloaded {} episodes".format(total_downloaded))


if __name__ == "__main__":
    __main__()
