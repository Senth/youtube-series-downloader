from argparse import Namespace
from os import path
from typing import Any, Pattern
import sys
import site
import importlib.util
import importlib.machinery
import argparse

_config_dir = path.join("config", __package__.replace("_", "-"))
_config_file = path.join(_config_dir, "config.py")
_example_file = path.join(_config_dir, "config.example.py")

# Search for config file in sys path
_sys_config = path.join(sys.prefix, _config_file)
_user_config_file = path.join(site.getuserbase(), _config_file)
_config_file = ""
if path.exists(_sys_config):
    _config_file = _sys_config
elif path.exists(_user_config_file):
    _config_file = _user_config_file
# User hasn't configured the program yet
else:
    _sys_config_example = path.join(sys.prefix, _example_file)
    _user_config_example = path.join(site.getuserbase(), _example_file)
    if not path.exists(_sys_config_example) and not path.exists(_user_config_example):
        print(
            f"Error: no configuration found. It should be here: '{_user_config_file}'"
        )
        print(f"run: locate {_example_file}")
        print("This should help you find the current config location.")
        print(
            "Otherwise you can download the config.example.py from https://github.com/Senth/youtube-series-downloader/tree/main/config and place it in the correct location"
        )
        sys.exit(1)

    print("This seems like it's the first time you run this program.")
    print(
        f"For this program to work properly you have to configure it by editing '{_user_config_file}'."
    )
    print(
        "In the same folder there's an example file 'config.example.py' you can copy to 'config.py'."
    )
    sys.exit(1)

# Import config
_loader = importlib.machinery.SourceFileLoader("config", _user_config_file)
_spec = importlib.util.spec_from_loader(_loader.name, _loader)
_user_config: Any = importlib.util.module_from_spec(_spec)
_loader.exec_module(_user_config)


def _print_missing(variable_name) -> None:
    print(f"Missing {variable_name} variable in config file: {_user_config_file}")
    print("Please add it to you config.py again to continue")
    sys.exit(1)


class Config:
    def __init__(self, user_config: Any) -> None:
        self._user_config = user_config
        self._set_default_values()
        self._get_optional_variables()
        self._check_required_variables()
        self._parse_args()
        self.app_name = __package__.replace("_", "-")

    def _parse_args(self) -> None:
        # Get arguments first to get verbosity before we get everything else
        parser = argparse.ArgumentParser()

        parser.add_argument(
            "-v", "--verbose", action="store_true", help="Prints out helpful messages."
        )
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
            help="Override the config settings with how many threads you want to use",
        )
        parser.add_argument(
            "-d",
            "--daemon",
            action="store_true",
            help="Run the script as a daemon instead of once",
        )
        parser.add_argument(
            "--max-days-back",
            type=int,
            help="How many days back we should check for videos",
        )
        parser.add_argument(
            "--debug",
            action="store_true",
            help="Turn on debug messages. This automatically turns on --verbose as well.",
        )

        _args = parser.parse_args()
        self._add_args_settings(_args)

    def _add_args_settings(self, args: Namespace) -> None:
        """Set additional configuration from script arguments

        Args:
            args (list): All the parsed arguments
        """
        self.verbose = args.verbose
        self.debug = args.debug
        self.pretend = args.pretend
        self.daemon = args.daemon

        if args.max_days_back:
            self.max_days_back = args.max_days_back

        if args.threads:
            self.threads = args.threads

        if args.debug:
            self.verbose = True

    def _set_default_values(self) -> None:
        """Set default values for variables"""
        self.threads = 1
        self.speed_up_default = 1
        self.max_days_back = 3

    def _get_optional_variables(self) -> None:
        """Get optional values from the config file"""
        try:
            self.threads = _user_config.THREADS
        except AttributeError:
            pass

        try:
            self.speed_up_default = _user_config.SPEED_UP_DEFAULT
        except AttributeError:
            pass

        try:
            self.max_days_back = _user_config.MAX_DAYS_BACK
        except AttributeError:
            pass

    def _check_required_variables(self) -> None:
        """Check that all required variables are set in the user config file"""
        try:
            self.series_dir = _user_config.SERIES_DIR
        except AttributeError:
            _print_missing("SERIES_DIR")

        try:
            self.channels = _user_config.CHANNELS
        except AttributeError:
            _print_missing("CHANNELS")

    def _check_channel_info(self) -> None:
        """Check so that the channel info is set correctly"""
        channel_example = "UCcJgOeune0II4a_qi9OMkRA"
        for name, info in self.channels:
            # Name is string
            if type(name) is not str:
                print(
                    f"Channel ({name}) name is not a string in config file: {_user_config_file}"
                )
                sys.exit(1)

            # Channel id required
            if "channel_id" in info:
                # Channel id valid format
                if type(info["channel_id"]) is not str or len(
                    info["channel_id"]
                ) != len(channel_example):
                    print(
                        f"Channel ({name}), channel_id ({info['channel_id']}) does not look like a valid channel id in config file: {_user_config_file}"
                    )
                    print(f"Here is an example of a channel id {channel_example}")
                    sys.exit(1)
            else:
                print(
                    f"Channel ({name}) missing channel_id in config file: {_user_config_file}"
                )
                sys.exit(1)

            # Dir (optional)
            if "dir" in info and type(info["dir"]) is not str:
                print(
                    f"Channel ({name}) dir ({info['dir']}) is not a string in config file: {_user_config_file}"
                )
                sys.exit(1)

            # Speed (optional)
            if (
                "speed" in info
                and type(info["speed"]) is not int
                and type(info["speed"]) is not float
            ):
                print(
                    f"Channel ({name}) speed ({info['speed']}) is not a number in config file {_user_config_file}"
                )
                sys.exit(1)

            # Include & Exclude (optional)
            Config._check_regex(name, "includes", info)
            Config._check_regex(name, "excludes", info)

    @staticmethod
    def _check_regex(channel_name: str, list_name: str, info: dict) -> None:
        """Check so include or exclude channel is set correctly

        Args:
            channel_name (str): The channel name
            list_name (str): Should be includes or excludes
            info (dict): Channel information
        """
        if list_name in info:
            # Should be a list
            if type(info[list_name]) is list:
                # All values should be regex
                for value in info[list_name]:
                    if not isinstance(value, Pattern):
                        print(
                            f"Channel ({channel_name}) has an invalid {list_name} item ({value}) that is not a Regex pattern in config file: {_user_config_file}"
                        )
                        sys.exit(1)
            else:
                print(
                    f"Channel ({channel_name}), {list_name} is not a list in config file: {_user_config_file}"
                )
                sys.exit(1)


global config
config = Config(_user_config)
