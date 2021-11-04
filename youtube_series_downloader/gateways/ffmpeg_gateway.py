import subprocess
from pathlib import Path
from shutil import copyfile
from tempfile import gettempdir
from typing import Union

from tealprint import TealLevel, TealPrint
from youtube_series_downloader.config import config
from youtube_series_downloader.core.video import Video


class FfmpegGateway:
    @staticmethod
    def render(video: Video, in_file: Path, out_file: Path, speed: float) -> bool:
        completed_process = True
        tmp_out = Path(gettempdir(), f"{video.id}_render_out.mp4")

        if not config.pretend:
            # Create parent directories
            out_file.parent.mkdir(parents=True, exist_ok=True)

            audio_speed = speed
            video_speed = 1.0 / audio_speed

            completed_process = (
                subprocess.run(
                    [
                        "ffmpeg",
                        "-y",
                        "-i",
                        in_file,
                        "-metadata",
                        f'title="{video.title}"',
                        "-threads",
                        str(config.general.threads),
                        "-filter_complex",
                        f"[0:v]setpts=({video_speed})*PTS[v];[0:a]atempo={audio_speed}[a]",
                        "-map",
                        "[v]",
                        "-map",
                        "[a]",
                        tmp_out,
                    ],
                    stdout=FfmpegGateway._get_verbose_out(),
                ).returncode
                == 0
            )

        if completed_process:
            # Copy the temprory file to series/Minecraft
            if not config.pretend:
                copyfile(tmp_out, out_file)

        TealPrint.debug("🗑 Deleting temporary files")
        in_file.unlink(missing_ok=True)
        tmp_out.unlink(missing_ok=True)

        return completed_process

    @staticmethod
    def _get_verbose_out() -> Union[int, None]:
        if config.general.log_level.value < TealLevel.verbose.value:
            return None
        else:
            return subprocess.DEVNULL
