from shutil import which
from platform import system


def check_for_programs():
    if which("ffmpeg") is None:
        print(
            "Could not find ffmpeg progam on your computer which is required to use this script."
        )

        # Print specific instructions for various OSes
        os = system()
        if os == "Windows" or os == "Darwin":
            print(
                "You can download and install the program from here: https://ffmpeg.org/download.html"
            )
            if os == "Window":
                print("Remember to add ffmpeg.exe to your PATH variable")
        elif os == "Linux":
            print("You can download it using your distributions package manager")

        exit(1)

    if which("youtube-dl") is None:
        print(
            "youtube-dl doesn't appear to be in your PATH variable. Please add it to your PATH variable."
        )
