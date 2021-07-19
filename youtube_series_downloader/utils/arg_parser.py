import argparse


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-p",
        "--pretend",
        action="store_true",
        help="Only pretend to download, convert, and store files.",
    )
    parser.add_argument(
        "-t",
        "--threads",
        type=int,
        help="How many threads you want to use (overrides file config).",
    )
    parser.add_argument(
        "-d",
        "--daemon",
        action="store_true",
        help="Run the script as a daemon instead of once.",
    )
    parser.add_argument(
        "--max-days-back",
        type=int,
        help="How many days back we should check for videos (overrides file config).",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Prints out helpful messages.",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Turn on debug messages. This automatically turns on --verbose as well.",
    )
    parser.add_argument(
        "-s",
        "--silent",
        action="store_true",
        help="Turns off all messages except errors.",
    )

    args = parser.parse_args()
    return args
