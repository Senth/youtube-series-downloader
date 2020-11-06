from __future__ import annotations
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
import logging
from .config import config
from .program_checker import check_for_programs
from .logger import LogColors, log_message
from .downloader import Downloader
from .channel import Channel
from .db import Db


def __main__():
    check_for_programs()

    # Set logger for apscheduler depending on verbosity
    if config.debug:
        logging.getLogger("apscheduler").setLevel(logging.DEBUG)
    elif config.verbose:
        logging.getLogger("apscheduler").setLevel(logging.INFO)
    else:
        logging.getLogger("apscheduler").setLevel(logging.ERROR)

    if config.daemon:
        log_message(f"Starting {config.app_name} as a daemon")
        _daemon()
    else:
        log_message(f"Running {config.app_name} once")
        _run_once()


def _daemon():
    scheduler = BlockingScheduler()
    scheduler.add_job(
        _run_once,
        "interval",
        minutes=10,
        max_instances=1,
        next_run_time=datetime.now(),
    )
    scheduler.start()


def _run_once():
    total_downloaded = 0
    db = Db()
    try:
        channels = Channel.create_from_config()
        for channel in channels:
            videos = channel.get_videos()

            for video in videos:
                downloader = Downloader(db, channel, video)

                if not downloader.has_downloaded():
                    downloader.download()
                    total_downloaded += 1
                else:
                    log_message(
                        f"Skipping {channel.name}, no new videos to download",
                        LogColors.skipped,
                    )
    except Exception as e:
        raise e
    finally:
        db.close()
    log_message("\n\nDownloaded {} episodes".format(total_downloaded), LogColors.added)


if __name__ == "__main__":
    __main__()
