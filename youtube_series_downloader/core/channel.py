from typing import List

from youtube_series_downloader.config import config


class Channel:
    def __init__(
        self,
        name: str = "",
        id: str = "",
        collection_dir: str = "",
        speed: float = config.general.speed_up_default,
        includes: List[str] = [],
        excludes: List[str] = [],
    ):
        self.name = name
        self.id = id
        self.collection_dir = collection_dir
        self.speed = speed
        self.includes = includes
        self.excludes = excludes
