from __future__ import annotations

import re
from datetime import datetime
from typing import List, Pattern

import requests

from .config import config
from .logger import LogColors, Logger
from .video import Video


class Channel:
    _RSS_PREFIX = "https://www.youtube.com/feeds/videos.xml?channel_id="
    _REGEX = re.compile(
        r"<entry>.*?<yt:videoId>(.*?)<\/yt:videoId>.*?<title>(.*?)<\/title>.*?<published>(.*?)<\/published>.*?<\/entry>",
        re.DOTALL,
    )

    def __init__(
        self,
        name: str,
        channel_id: str,
        collection_dir: str,
        speed: float,
        excludes: List[Pattern],
        includes: List[Pattern],
    ):
        self.name = name
        self.channel_id = channel_id
        self.collection_dir = collection_dir
        self.speed = speed
        self.excludes = excludes
        self.includes = includes

    @staticmethod
    def create_from_config() -> List[Channel]:
        channels = list()

        for name, info in config.channels.items():
            channel_id = info["channel_id"]

            if "dir" in info:
                dir = info["dir"]
            else:
                dir = ""

            if "speed" in info:
                speed = info["speed"]
            else:
                speed = config.speed_up_default

            if "includes" in info:
                includes = info["includes"]
            else:
                includes = []

            if "excludes" in info:
                excludes = info["excludes"]
            else:
                excludes = []

            channel = Channel(
                name=name,
                channel_id=channel_id,
                collection_dir=dir,
                speed=speed,
                includes=includes,
                excludes=excludes,
            )
            channels.append(channel)

        return channels

    def get_videos(self) -> List[Video]:
        if config.verbose:
            Logger.verbose("".ljust(40, "*"))
            Logger.verbose(self.name.center(40), LogColors.header)
            Logger.verbose("".ljust(40, "*"))

        else:
            Logger.info(self.name, LogColors.header)

        url = Channel._RSS_PREFIX + self.channel_id
        xml = requests.get(url).text

        matches = Channel._REGEX.findall(xml)
        matches.reverse()

        videos = []

        for groups in matches:
            id = groups[0]
            title = groups[1]
            date = groups[2]
            Logger.verbose(f"🔎 Checking video {id} {LogColors.bold}{title}{LogColors.no_color} — {date}")

            if self._is_new(date) and self._matches_includes(title) and not self._matches_excludes(title):
                video = Video(id, date, title)
                Logger.info(f"➕ {title}", LogColors.added)
                videos.append(video)

        return videos

    def _is_new(self, dateString: str) -> bool:
        # If config is set to 0. All episodes are new
        if config.max_days_back == 0:
            return True
        else:
            date = datetime.strptime(dateString, "%Y-%m-%dT%H:%M:%S%z")
            diff_time = datetime.now() - date.replace(tzinfo=None)

            if diff_time.days <= config.max_days_back:
                Logger.verbose(f"🟢 New by {diff_time.days} days", LogColors.passed, indent=1)
                return True
            else:
                Logger.verbose(f"🔴 Old by {diff_time.days} days", LogColors.skipped, indent=1)
                return False

    def _matches_excludes(self, title: str) -> bool:
        for filter in self.excludes:
            if re.search(filter, title):
                Logger.verbose(f"🔴 Exclude: {filter}", LogColors.skipped, indent=1)
                return True

        Logger.verbose("🟢 No matching excludes", LogColors.passed, indent=1)
        return False

    def _matches_includes(self, title: str) -> bool:
        if len(self.includes) == 0:
            return True

        for filter in self.includes:
            if re.search(filter, title):
                Logger.verbose(f"🟢 Include: {filter}", LogColors.passed, indent=1)
                return True

        Logger.verbose("🔴 No matching includes", LogColors.skipped, indent=1)
        return False
