import re
import subprocess
from os import makedirs, path, remove
from shutil import copyfile
from subprocess import run
from tempfile import gettempdir
from typing import Union

from tealprint import TealPrint
from tealprint.tealprint import TealLevel

from .channel import Channel
from .config import config
from .db import Db
from .log_colors import LogColors
from .video import Video


class Downloader:
    def __init__(self, db: Db, channel: Channel, video: Video):
        self._db = db
        self._video = video
        self._channel = channel
        self._tmp_download = path.join(gettempdir(), self._video.id + ".mkv")
        self._tmp_converted = path.join(gettempdir(), self._video.id + ".mp4")

    def has_downloaded(self) -> bool:
        """Check if this video has been downloaded

        Returns:
            bool: True if it has been downloaded before
        """
        return self._db.has_downloaded(self._video.id)

    def download(self):
        """Download and convert the video"""

        # Download video
        completed_process = True

        if not config.pretend:
            self._tmp_download

            completed_process = (
                run(
                    [
                        "youtube-dl",
                        "-o",
                        self._tmp_download,
                        "--merge-output-format",
                        "mkv",
                        "--restrict-filenames",
                        "--",
                        self._video.id,
                    ],
                    stdout=self._get_verbose_out(),
                ).returncode
                == 0
            )

        # Convert and save video
        if completed_process:
            self._convert()
        else:
            TealPrint.info(
                f"Failed to download video {self._video.title} - {self._video.id}, from channel {self._channel.name}",
                color=LogColors.error,
            )

        TealPrint.debug("Out filepath: " + str(self._get_out_filepath()))

    def _convert(self):
        out_filepath = self._get_out_filepath()
        completed_process = True

        TealPrint.info(f"🎞 Re-rendering to different speeds", indent=1)
        if not config.pretend:
            self._create_out_dir()
            audio_speed = self._channel.speed
            video_speed = 1.0 / audio_speed

            completed_process = (
                run(
                    [
                        "ffmpeg",
                        "-i",
                        self._tmp_download,
                        "-metadata",
                        f'title="{self._video.title}"',
                        "-threads",
                        str(config.threads),
                        "-filter_complex",
                        f"[0:v]setpts=({video_speed})*PTS[v];[0:a]atempo={audio_speed}[a]",
                        "-map",
                        "[v]",
                        "-map",
                        "[a]",
                        self._tmp_converted,
                    ],
                    stdout=self._get_verbose_out(),
                ).returncode
                == 0
            )

        if completed_process:
            # Copy the temprory file to series/Minecraft
            TealPrint.info(f"💾 Saving rendered video ➡ {out_filepath}", indent=1)
            if not config.pretend:
                copyfile(self._tmp_converted, out_filepath)

            # Delete temporary files original file
            TealPrint.debug("🗑 Deleting temporary files", indent=1)
            if not config.pretend:
                remove(self._tmp_converted)
                remove(self._tmp_download)

            self._db.add_downloaded(self._channel.name, self._video.id)

    def _get_out_dir(self) -> str:
        return path.join(
            config.general.series_dir,
            self._channel.collection_dir,
            self._channel.name,
            "Season 01",
        )

    def _create_out_dir(self):
        makedirs(self._get_out_dir(), exist_ok=True)

    def _get_filename_safe(self) -> str:
        # Replace : or | with -
        title = re.sub(r"[:\|]", " -", self._video.title)

        # Remove illegal characters
        title = re.sub(r"[^\w\ \-\.,]", "", title)

        # Remove all places where there are two whitespaces
        title = " ".join(title.split())

        return title

    def _get_out_filepath(self) -> str:
        episode_number = self._db.get_next_episode_number(self._channel.name)
        out_filename = "{} - s01e{} - {}.mp4".format(self._channel.name, episode_number, self._get_filename_safe())
        out_filepath = path.join(self._get_out_dir(), out_filename)

        return out_filepath
