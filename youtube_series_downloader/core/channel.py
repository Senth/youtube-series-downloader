from typing import List, Optional

from youtube_series_downloader.config import config


class Channel:
    def __init__(
        self,
        name: str = "",
        id: str = "",
        collection_dir: str = "",
        speed: Optional[float] = None,
        includes: List[str] = [],
        excludes: List[str] = [],
    ):
        self.name = name
        self.id = id
        self.collection_dir = collection_dir
        self.includes = includes
        self.excludes = excludes
        if speed:
            self.speed: float = speed
        else:
            self.speed: float = config.general.speed_up_default
