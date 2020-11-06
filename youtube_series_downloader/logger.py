from .config import config


def log_message(message: str):
    """Log message if verbose has been set to true

    Args:
        message (str): The message to log
    """
    if config.verbose:
        print(message)
