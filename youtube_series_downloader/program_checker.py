from platform import system
from shutil import which
from sys import exit

from tealprint import TealPrint


def check_for_programs():
    if which("ffmpeg") is None:
        TealPrint.warning("Could not find ffmpeg progam on your computer which is required to use this script.")

        # Print specific instructions for various OSes
        os = system()
        if os == "Windows" or os == "Darwin":
            TealPrint.info("You can download and install the program from here: https://ffmpeg.org/download.html")
            if os == "Window":
                TealPrint.info("Remember to add ffmpeg.exe to your PATH variable")
        elif os == "Linux":
            TealPrint.info("You can download it using your distributions package manager")

        exit(1)

    if which("youtube-dl") is None:
        TealPrint.warning(
            "youtube-dl doesn't appear to be in your PATH variable. Please add it to your PATH variable.", exit=True
        )
