import argparse
from argparse import Namespace

from tealprint import TealLevel, TealPrint


class Config:
    def __init__(self) -> None:

        self.threads = 1
        self.speed_up_default = 1
        self.max_days_back = 3
        self.general = General()
        self.level: TealLevel = TealLevel.info
        self.pretend: bool
        self.daemon: bool

        self._parse_args()
        self.app_name = __package__.replace("_", "-")

    def _parse_args(self) -> None:
        # Get arguments first to get verbosity before we get everything else
        parser = argparse.ArgumentParser()

        parser.add_argument(
            "-p",
            "--pretend",
            action="store_true",
            help="Only pretend to download, convert, and store files.",
        )
        parser.add_argument(
            "-t",
            "--threads",
            type=int,
            help="How many threads you want to use (overrides file config).",
        )
        parser.add_argument(
            "-d",
            "--daemon",
            action="store_true",
            help="Run the script as a daemon instead of once.",
        )
        parser.add_argument(
            "--max-days-back",
            type=int,
            help="How many days back we should check for videos (overrides file config).",
        )
        parser.add_argument(
            "-v",
            "--verbose",
            action="store_true",
            help="Prints out helpful messages.",
        )
        parser.add_argument(
            "--debug",
            action="store_true",
            help="Turn on debug messages. This automatically turns on --verbose as well.",
        )
        parser.add_argument(
            "-s",
            "--silent",
            action="store_true",
            help="Turns off all messages except errors.",
        )

        _args = parser.parse_args()
        self._add_args_settings(_args)

    def _add_args_settings(self, args: Namespace) -> None:
        """Set additional configuration from script arguments

        Args:
            args (list): All the parsed arguments
        """
        if args.debug:
            self.level = TealLevel.debug
        elif args.verbose:
            self.level = TealLevel.verbose
        elif args.silent:
            self.level = TealLevel.warning
        TealPrint.level = self.level

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


config = Config()
