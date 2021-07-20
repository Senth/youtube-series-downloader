from pathlib import Path
from typing import List, Optional

from youtube_series_downloader.app.download_new_episodes.download_new_episodes_repo import (
    DownloadNewEpisodesRepo,
)
from youtube_series_downloader.core.channel import Channel
from youtube_series_downloader.core.video import Video
from youtube_series_downloader.gateways.ffmpeg_gateway import FfmpegGateway
from youtube_series_downloader.gateways.sqlite_gateway import SqliteGateway
from youtube_series_downloader.gateways.youtube_dl_gateway import YoutubeDlGateway
from youtube_series_downloader.gateways.youtube_gateway import YoutubeGateway


class AppAdapter(DownloadNewEpisodesRepo):
    def __init__(self) -> None:
        self.sqlite_gateway = SqliteGateway()

    def close(self) -> None:
        self.sqlite_gateway.close()

    def get_latest_videos(self, channel: Channel) -> List[Video]:
        return YoutubeGateway.get_videos(channel)

    def has_downloaded(self, video: Video) -> bool:
        return self.sqlite_gateway.has_downloaded(video.id)

    def set_as_downloaded(self, channel: Channel, video: Video) -> None:
        return self.sqlite_gateway.add_downloaded(channel.name, video.id)

    def get_next_episode_number(self, channel: Channel) -> int:
        return self.sqlite_gateway.get_next_episode_number(channel.name)

    def download(self, video: Video) -> Optional[Path]:
        return YoutubeDlGateway.download(video)

    def render(self, video: Video, in_file: Path, out_file: Path, speed: float) -> bool:
        return FfmpegGateway.render(video, in_file, out_file, speed)
