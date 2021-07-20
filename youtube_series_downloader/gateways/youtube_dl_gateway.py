from pathlib import Path
from tempfile import gettempdir
from typing import Optional

from youtube_dl import YoutubeDL
from youtube_series_downloader.config import config
from youtube_series_downloader.core.video import Video


class YoutubeDlGateway:
    @staticmethod
    def download(video: Video) -> Optional[Path]:
        out_file = Path(gettempdir(), f"{video.id}.mkv")

        if config.pretend:
            return out_file

        ydl_opts = {
            "outtmpl": str(out_file),
            "merge_output_formats": "mkv",
        }
        with YoutubeDL(ydl_opts) as ydl:
            return_code = ydl.download([video.id])
            if return_code == 0:
                return out_file

        return None
