import enum
from enum import Enum
from .config import config


class LogColors:
    no_color = "\033[0m"
    red = "\033[91m"
    green = "\033[92m"
    cyan = "\033[96m"
    blue = "\033[94m"
    yellow = "\033[33m"

    header = yellow
    skipped = red
    added = green
    passed = cyan


def log_message(message: str, color: str = LogColors.no_color):
    """Log message if verbose has been set to true

    Args:
        message (str): The message to log
        color (LogColors): Optional color of the message
    """
    if config.verbose:
        if color == LogColors.no_color:
            print(message)
        else:
            print(f"{color}{message}{LogColors.no_color}")


def debug_message(message: str, color: str = LogColors.no_color):
    """A debug message if --debug has been set to true

    Args:
        message (str): The message to log
        color (LogColors): Optional color of the message
    """
    if config.debug:
        if color == LogColors.no_color:
            print(message)
        else:
            print(f"{color}{message}{LogColors.no_color}")
