import subprocess
import sys
from tempfile import gettempdir
from .db import Db
from .video import Video
from .channel import Channel
from .logger import log_message
from .config import config
from subprocess import run
from shutil import copyfile
from os import path, makedirs, remove
import re


class Downloader:
    _db = Db()

    def __init__(self, channel: Channel, video: Video):
        self._video = video
        self._channel = channel
        self._tmp_download = path.join(gettempdir(), self._video.id + ".mkv")
        self._tmp_converted = path.join(gettempdir(), self._video.id + ".mp4")

    def has_downloaded(self) -> bool:
        """Check if this video has been downloaded

        Returns:
            bool: True if it has been downloaded before
        """
        return Downloader._db.has_downloaded(self._video.id)

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
                        "-f",
                        "bestvideo[height>=1080,fps=60]+bestaudio",
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
            print(
                "Failed to download video {} - {}, from channel {}".format(
                    self._video.title, self._video.id, self._channel.name
                ),
                file=sys.stderr,
            )

        log_message("Out filepath: " + str(self._get_out_filepath()))

    def _convert(self):
        out_filepath = self._get_out_filepath()
        converted = False

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
                        'title="{}"'.format(self._video.title),
                        "-threads",
                        str(config.threads),
                        "-filter_complex",
                        "[0:v]setpts=({})*PTS[v];[0:a]atempo={}[a]".format(
                            video_speed, audio_speed
                        ),
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
                converted = True
                # Copy the temprory file to series/Minecraft
                log_message(
                    "Copying file {} to {}".format(self._video.id, out_filepath)
                )
                copyfile(self._tmp_converted, out_filepath)

                # Delete temporary files original file
                log_message("{} Deleting temporary files".format(self._video.id))
                remove(self._tmp_converted)
                remove(self._tmp_download)

        if converted or config.pretend:
            Downloader._db.add_downloaded(self._channel.name, self._video.id)

    def _get_verbose_out(self) -> int:
        if config.verbose:
            return subprocess.STDOUT
        else:
            return subprocess.DEVNULL

    def _get_out_dir(self) -> str:
        return path.join(
            config.series_dir,
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
        episode_number = Downloader._db.get_next_episode_number(self._channel.name)
        out_filename = "{} - s01e{} - {}.mp4".format(
            self._channel.name, episode_number, self._get_filename_safe()
        )
        out_filepath = path.join(self._get_out_dir(), out_filename)

        return out_filepath
