from __future__ import annotations

import logging
from datetime import datetime

from apscheduler.schedulers.blocking import BlockingScheduler
from tealprint import TealPrint
from tealprint.tealprint import TealLevel

from youtube_series_downloader import config_gateway

from .channel import Channel
from .config import Config, config
from .config_gateway import ConfigGateway
from .db import Db
from .downloader import Downloader
from .log_colors import LogColors
from .program_checker import check_for_programs


def main():
    check_for_programs()

    # Set logger for apscheduler depending on verbosity
    if config.level == TealLevel.debug:
        logging.getLogger("apscheduler").setLevel(logging.DEBUG)
    elif config.level == TealLevel.verbose:
        logging.getLogger("apscheduler").setLevel(logging.INFO)
    else:
        logging.getLogger("apscheduler").setLevel(logging.ERROR)

    if config.daemon:
        TealPrint.verbose(f"Starting {config.app_name} as a daemon")
        _daemon()
    else:
        TealPrint.verbose(f"Running {config.app_name} once")
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
    config_gateway = ConfigGateway()
    config_gateway.setGeneral(config.general)
    channels = config_gateway.getChannels()
    try:
        for channel in channels:
            videos = channel.get_videos()

            TealPrint.info(channel.name, color=LogColors.header)

            if len(videos) == 0:
                TealPrint.info(
                    f"🦘 Skipping {channel.name}, no new matching videos to download", color=LogColors.skipped, indent=1
                )

            for video in videos:
                downloader = Downloader(db, channel, video)

                if not downloader.has_downloaded():
                    downloader.download()
                    total_downloaded += 1
                else:
                    TealPrint.verbose(
                        f"🟠 Skipping {video.title}, already downloaded", color=LogColors.skipped, indent=1
                    )

            TealPrint.info("")
    except Exception as e:
        raise e
    finally:
        db.close()
    TealPrint.info(f"\n\nDownloaded {total_downloaded} episodes", color=LogColors.added)


if __name__ == "__main__":
    main()
