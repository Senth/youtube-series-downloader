import os
import platform
from pathlib import Path
from subprocess import run
from sys import exit
from typing import List

from blulib.config_parser import ConfigParser
from tealprint import TealPrint

from .channel import Channel
from .config import General, config


class ConfigGateway:
    def __init__(self) -> None:
        path = Path.home().joinpath(f".{config.app_name}.cfg")
        self.parser = ConfigParser()

        if not path.exists():
            TealPrint.info(f"Could not find any configuration file in {path}")
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
                run([editor, path])

            else:
                exit(0)

        self.parser.read(path)

    def setGeneral(self, general: General) -> None:
        self.parser.to_object(
            general,
            "General",
            "series_dir",
            "threads",
            "speed_up_default",
            "max_days_back",
        )

    def getChannels(self) -> List[Channel]:
        channels: List[Channel] = []
        for section in self.parser.sections():
            if ConfigGateway.isChannelSection(section):
                channel = Channel()
                self.parser.to_object(
                    channel,
                    section,
                    "channel_id",
                    "dir",
                    "float:speed",
                    "str_list:includes",
                    "str_list:excludes",
                )
                channels.append(channel)
        return channels

    @staticmethod
    def isChannelSection(section: str) -> bool:
        return section != "General" and section != "DEFAULT" and section != "vars"
