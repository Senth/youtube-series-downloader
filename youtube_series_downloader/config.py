from argparse import Namespace

from tealprint import TealLevel, TealPrint


class Config:
    def __init__(self) -> None:
        self.general = General()
        self.level: TealLevel = TealLevel.info
        self.pretend: bool = False
        self.daemon: bool = False
        self.app_name = __package__.replace("_", "-")

    def set_cli_args(self, args: Namespace) -> None:
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
