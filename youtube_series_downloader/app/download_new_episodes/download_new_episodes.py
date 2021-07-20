import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import List

from tealprint import TealLevel, TealPrint
from youtube_series_downloader.app.download_new_episodes.download_new_episodes_repo import (
    DownloadNewEpisodesRepo,
)
from youtube_series_downloader.config import config
from youtube_series_downloader.core.channel import Channel
from youtube_series_downloader.core.video import Video
from youtube_series_downloader.utils.log_colors import LogColors


class DownloadNewEpisodes:
    def __init__(self, repo: DownloadNewEpisodesRepo) -> None:
        self.repo = repo

    def execute(self, channels: List[Channel]) -> None:
        for channel in channels:
            TealPrint.info(channel.name, color=LogColors.header)

            videos = self.repo.get_latest_videos(channel)

            if len(videos) == 0:
                TealPrint.info(
                    f"🦘 Skipping {channel.name}, no new matching videos to download", color=LogColors.skipped, indent=1
                )

            for video in videos:
                indent = 1
                if config.level.value >= TealLevel.verbose.value:
                    indent = 2
                TealPrint.verbose(f"🎞 {video.title}", color=LogColors.header, indent=1)

                # Skip downloaded videos
                if self.repo.has_downloaded(video):
                    TealPrint.verbose(
                        f"🟠 Skipping {video.title}, already downloaded", color=LogColors.skipped, indent=indent
                    )
                    continue

                # Filter out
                if self._filter_video(channel, video):
                    TealPrint.verbose(f"🔴 Video was filtered out", color=LogColors.filtered, indent=indent)
                    continue
                TealPrint.verbose(f"🟢 Video passed all filters", color=LogColors.passed, indent=indent)

                TealPrint.verbose(f"🔽 Downloading...", indent=indent)
                download_path = self.repo.download(video)

                if download_path is None:
                    TealPrint.warning(f"⚠ Couldn't download {video.title}", indent=indent)
                    continue

                TealPrint.verbose(f"🎞 Starting rendering, this may take a while...", indent=indent)
                out_path = self._get_out_filepath(channel, video)
                rendered = self.repo.render(video, download_path, out_path, channel.speed)

                if not rendered:
                    TealPrint.warning(f"⚠ Couldn't render {video.title}", indent=indent)
                    continue

                self.repo.set_as_downloaded(channel, video)
                TealPrint.info(f"✔ Video {video.title} downloaded successfully ➡ {out_path}", indent=indent)

    def _get_out_filepath(self, channel: Channel, video: Video) -> Path:
        title = self._get_safe_video_title(video)
        episode_number = self.repo.get_next_episode_number(channel)
        filename = f"{channel.name} - s01e{episode_number} - {title}.mp4"

        return Path(
            config.general.series_dir,
            channel.collection_dir,
            channel.name,
            "Season 01",
            filename,
        )

    def _get_safe_video_title(self, video: Video) -> str:
        # Replace : or | with -
        title = re.sub(r"[:\|]", " -", video.title)

        # Remove illegal characters
        title = re.sub(r"[^\w\ \-\.,]", "", title)

        # Remove all places where there are two whitespaces
        title = " ".join(title.split())

        return title

    def _filter_video(self, channel: Channel, video: Video) -> bool:
        """Return true if the video should be filtered out"""

        if self._is_old(video):
            return True

        if not self._matches_any_include(channel, video):
            return True

        if self._matches_any_exclude(channel, video):
            return True

        return False

    def _is_old(self, video: Video) -> bool:
        TealPrint.verbose(f"🚦 Is the video old?", indent=2)

        old_date = datetime.now().astimezone() - timedelta(days=config.general.max_days_back)
        video_date = datetime.strptime(video.date, "%Y-%m-%dT%H:%M:%S%z")

        if video_date >= old_date:
            TealPrint.verbose(f"🟢 Video is new", color=LogColors.passed, indent=3)
            return False
        else:
            TealPrint.verbose(f"🔴 Video is old", color=LogColors.filtered, indent=3)
            return True

    def _matches_any_include(self, channel: Channel, video: Video) -> bool:
        title = video.title.lower()
        TealPrint.verbose(f"🚦 Check include filter", indent=2)

        if len(channel.includes) == 0:
            TealPrint.verbose(f"🟢 Pass: no include filter", color=LogColors.passed, indent=3)
            return True

        for filter in channel.includes:
            filter = filter.lower()
            if re.search(filter, title):
                TealPrint.verbose(f"🟢 Pass include: {filter}", color=LogColors.passed, indent=3)
                return True
            else:
                TealPrint.verbose(f"🟡 Didn't match filter: {filter}", color=LogColors.no_match, indent=3)

        TealPrint.verbose(f"🔴 Filtered: didn't match any include filter", color=LogColors.filtered, indent=3)
        return False

    def _matches_any_exclude(self, channel: Channel, video: Video) -> bool:
        title = video.title.lower()
        TealPrint.verbose(f"🚦 Check exclude filter", indent=2)

        if len(channel.excludes) == 0:
            TealPrint.verbose(f"🟢 Pass: no exclude filter", color=LogColors.passed, indent=3)
            return False

        for filter in channel.excludes:
            filter = filter.lower()
            if re.search(filter, title):
                TealPrint.verbose(f"🔴 Matched filter: {filter}", color=LogColors.filtered, indent=3)
                return True
            else:
                TealPrint.verbose(f"🟡 Didn't match filter: {filter}", color=LogColors.no_match, indent=3)

        TealPrint.verbose(f"🟢 Didn't match any exclude filter", color=LogColors.passed, indent=3)
        return False
