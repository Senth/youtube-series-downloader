from pathlib import Path
from tempfile import gettempdir
from typing import Optional

from tealprint.tealprint import TealLevel
from youtube_series_downloader.config import config
from youtube_series_downloader.core.video import Video
from yt_dlp import YoutubeDL


class YoutubeDlGateway:
    @staticmethod
    def download(video: Video) -> Optional[Path]:
        out_file = Path(gettempdir(), f"{video.id}.mkv")

        if config.pretend:
            return out_file

        quiet = config.general.log_level.value >= TealLevel.verbose.value
        no_warnings = config.general.log_level.value >= TealLevel.warning.value
        verbose = config.general.log_level.value >= TealLevel.debug.value

        ydl_opts = {
            "outtmpl": str(out_file),
            "quiet": quiet,
            "verbose": verbose,
            "no_warnings": no_warnings,
            "merge_output_format": "mkv",
        }
        if config.general.cookies_file:
            ydl_opts["cookies"] = config.general.cookies_file

        with YoutubeDL(ydl_opts) as ydl:
            return_code = ydl.download([video.id])
            if return_code == 0:
                return out_file

        return None
