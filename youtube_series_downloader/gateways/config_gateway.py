import os
import platform
from configparser import ExtendedInterpolation
from pathlib import Path
from subprocess import run
from sys import exit
from typing import List

from blulib.config_parser import ConfigParser
from tealprint import TealPrint
from tealprint.teallevel import TealLevel
from youtube_series_downloader.config import General, config
from youtube_series_downloader.core.channel import Channel


class ConfigGateway:
    def __init__(self) -> None:
        self.path = Path.home().joinpath(f".{config.app_name}.cfg")
        self.parser = ConfigParser(interpolation=ExtendedInterpolation())

    def check_config_exists(self) -> None:
        if not self.path.exists():
            TealPrint.info(f"Could not find any configuration file in {self.path}")
            user_input = input("Do you want to copy the example config and edit it (y/n)?")
            if user_input.lower() == "y":
                self.parser.copy_example_if_conf_not_exists(config.app_name)
                editor = ""
                if "EDITOR" in os.environ:
                    editor = os.environ["EDITOR"]
                if editor == "" and platform.system() == "Windows":
                    editor = "notepad.exe"
                elif editor == "":
                    editor = "vim"
                run([editor, self.path])

            else:
                exit(0)

    def read(self):
        self.parser.read(self.path)

    def get_general(self) -> General:
        general = General()
        self.parser.to_object(
            general,
            "General",
            "series_dir",
            "int:threads",
            "float:speed_up_default",
            "int:max_days_back",
            "log_level",
            "cookies_file",
        )
        if not general.series_dir:
            TealPrint.warning(
                f"Missing 'series_dir' in [General] in your configuration. Please add it.",
                exit=True,
            )

        # Convert string to LogLevel
        if isinstance(general.log_level, str):
            try:
                general.log_level = TealLevel[general.log_level]
            except KeyError:
                TealPrint.warning(
                    f"Failed to set log_level from config, invalid level: {general.log_level}. Setting log_level to info"
                )
                general.log_level = TealLevel.info

        return general

    def get_channels(self) -> List[Channel]:
        channels: List[Channel] = []
        for section in self.parser.sections():
            if ConfigGateway.is_channel_section(section):
                channel = Channel()
                channel.name = section
                self.parser.to_object(
                    channel,
                    section,
                    "id",
                    "name",
                    "dir->collection_dir",
                    "float:speed",
                    "str_list:includes",
                    "str_list:excludes",
                )

                if not channel.id:
                    TealPrint.warning(
                        f"Missing 'id' for channel [{section}] in your configuration. Please add it.",
                        exit=True,
                    )

                channels.append(channel)
        return channels

    @staticmethod
    def is_channel_section(section: str) -> bool:
        return section != "General" and section != "DEFAULT" and section != "vars"
