from __future__ import annotations

from argparse import Namespace

from tealprint import TealConfig, TealLevel


class Config:
    def __init__(self) -> None:
        self._general = General()
        self.pretend: bool = False
        self.daemon: bool = False
        self.app_name = __package__.replace("_", "-")

    @property
    def general(self) -> General:
        return self._general

    @general.setter
    def general(self, general: General) -> None:
        self._general = general
        TealConfig.level = general.log_level

    def set_cli_args(self, args: Namespace) -> None:
        """Set additional configuration from script arguments

        Args:
            args (list): All the parsed arguments
        """
        if args.debug:
            self.general.log_level = TealLevel.debug
        elif args.verbose:
            self.general.log_level = TealLevel.verbose
        elif args.silent:
            self.general.log_level = TealLevel.warning
        TealConfig.level = self.general.log_level

        self.pretend = args.pretend
        self.daemon = args.daemon

        if args.max_days_back:
            self.general.max_days_back = args.max_days_back

        if args.threads:
            self.general.threads = args.threads


class General:
    def __init__(self) -> None:
        self.series_dir: str = ""
        self.threads: int = 1
        self.speed_up_default: float = 1.0
        self.max_days_back: int = 3
        self.log_level = TealLevel.info
        self.cookies_file: str = ""


config = Config()
