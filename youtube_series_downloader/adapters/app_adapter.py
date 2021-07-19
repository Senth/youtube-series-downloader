from pathlib import Path
from typing import List

from youtube_series_downloader.app.download_new_episodes.download_new_episodes_repo import (
    DownloadNewEpisodesRepo,
)
from youtube_series_downloader.core.channel import Channel
from youtube_series_downloader.core.video import Video
from youtube_series_downloader.gateways.sqlite_gateway import SqliteGateway
from youtube_series_downloader.gateways.youtube_gateway import YoutubeGateway


class AppAdapter(DownloadNewEpisodesRepo):
    def __init__(self) -> None:
        self.youtube_gateway = YoutubeGateway()
        self.sqlite_gateway = SqliteGateway()
        
    def close(self) -> None:
        self.sqlite_gateway.close()
    
    def get_latest_videos(self, channel: Channel) -> List[Video]:
        return self.youtube_gateway.get_videos(channel)

    def has_downloaded(self, video: Video) -> bool:
        return self.sqlite_gateway.has_downloaded(video.id)
    
    def set_as_downloaded(self, channel: Channel, video: Video) -> None:
        return self.sqlite_gateway.add_downloaded(channel.name, video.id)
    
    def download(self, video: Video) -> Path:
        return super().download(video)
    
    def render(self, in: Path, out: Path, title: str, speed: float) -> None:
        return super().render(in, out, title, speed)
