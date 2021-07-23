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

    def __members(self):
        return (
            self.name,
            self.id,
            self.collection_dir,
            self.speed,
            self.includes,
            self.excludes,
        )

    def __eq__(self, other) -> bool:
        if type(other) is type(self):
            return self.__members() == other.__members()
        return False

    def __hash__(self) -> int:
        return hash(self.__members())

    def __repr__(self) -> str:
        return str(self.__members())
