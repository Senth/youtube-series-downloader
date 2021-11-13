from __future__ import annotations

import logging
from datetime import datetime

from apscheduler.schedulers.blocking import BlockingScheduler
from tealprint import TealPrint
from tealprint.tealprint import TealLevel

from youtube_series_downloader.adapters.app_adapter import AppAdapter
from youtube_series_downloader.app.download_new_episodes.download_new_episodes import (
    DownloadNewEpisodes,
)
from youtube_series_downloader.config import config
from youtube_series_downloader.gateways.config_gateway import ConfigGateway
from youtube_series_downloader.utils.arg_parser import get_args
from youtube_series_downloader.utils.program_checker import check_for_programs

config_gateway = ConfigGateway()


def main():
    check_for_programs()
    config.set_cli_args(get_args())
    config_gateway.check_config_exists()
    init_logs()

    if config.daemon:
        TealPrint.verbose(f"Starting {config.app_name} as a daemon")
        _daemon()
    else:
        TealPrint.verbose(f"Running {config.app_name} once")
        _run_once()


def init_logs():
    # Set logger for apscheduler depending on verbosity
    if config.general.log_level == TealLevel.debug:
        logging.getLogger("apscheduler").setLevel(logging.DEBUG)
    elif config.general.log_level == TealLevel.verbose:
        logging.getLogger("apscheduler").setLevel(logging.INFO)
    else:
        logging.getLogger("apscheduler").setLevel(logging.ERROR)


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
    # (Re)load config
    config_gateway.read()
    config.general = config_gateway.get_general()
    channels = config_gateway.get_channels()

    app_repo = AppAdapter()

    try:
        download_new_episodes = DownloadNewEpisodes(app_repo)
        download_new_episodes.execute(channels)
    finally:
        TealPrint.clear_indent()
        app_repo.close()


if __name__ == "__main__":
    main()
