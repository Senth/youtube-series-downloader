from __future__ import annotations

import logging
from datetime import datetime

from apscheduler.schedulers.blocking import BlockingScheduler

from .channel import Channel
from .config import config
from .db import Db
from .downloader import Downloader
from .logger import LogColors, Logger
from .program_checker import check_for_programs


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
        Logger.verbose(f"Starting {config.app_name} as a daemon")
        _daemon()
    else:
        Logger.verbose(f"Running {config.app_name} once")
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

            if len(videos) == 0:
                Logger.info(
                    f"🦘 Skipping {channel.name}, no new matching videos to download",
                    LogColors.skipped,
                )

            for video in videos:
                downloader = Downloader(db, channel, video)

                if not downloader.has_downloaded():
                    downloader.download()
                    total_downloaded += 1
                else:
                    Logger.verbose(
                        f"🟠 Skipping {video.title}, already downloaded",
                        LogColors.skipped,
                    )

            Logger.info("")
            Logger.verbose("")
    except Exception as e:
        raise e
    finally:
        db.close()
    Logger.info(f"\n\nDownloaded {total_downloaded} episodes", LogColors.added)


if __name__ == "__main__":
    __main__()
