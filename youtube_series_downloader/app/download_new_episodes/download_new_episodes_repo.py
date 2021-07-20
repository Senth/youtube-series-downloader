from pathlib import Path
from typing import List, Optional

from youtube_series_downloader.core.channel import Channel
from youtube_series_downloader.core.video import Video


class DownloadNewEpisodesRepo:
    def get_latest_videos(self, channel: Channel) -> List[Video]:
        raise NotImplementedError()

    def has_downloaded(self, video: Video) -> bool:
        raise NotImplementedError()

    def set_as_downloaded(self, channel: Channel, video: Video) -> None:
        raise NotImplementedError()

    def get_next_episode_number(self, channel: Channel) -> int:
        raise NotImplementedError()

    def download(self, video: Video) -> Optional[Path]:
        raise NotImplementedError()

    def render(self, video: Video, in_file: Path, out_file: Path, speed: float) -> bool:
        raise NotImplementedError()
