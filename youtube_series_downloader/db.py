from os import path
from pathlib import Path
import sqlite3
from .logger import log_message
from .config import config


class Db:
    _FILE_PATH = path.expanduser("~/.youtube-series.downloader.db")
    _FILE = Path(_FILE_PATH)

    def __init__(self):
        log_message("Sqlite DB location: {}".format(Db._FILE_PATH))
        self._connection = sqlite3.connect(Db._FILE_PATH)
        self._cursor = self._connection.cursor()

        # Create DB (if not exists)
        self._create_db()

    def _create_db(self):
        self._connection.execute(
            "Create TABLE IF NOT EXISTS video (id TEXT, episode_number INTEGER, channel_name TEXT)"
        )
        self._connection.commit()

    def add_downloaded(self, channel_name: str, video_id: str):
        """Adds a downloaded episode to the DB

        Args:
            channel_name (str): Channel name (not channel_id)
            video_id (str): YouTube's video id for the video that was downloaded
        """
        episode_number = self.get_next_episode_number(channel_name)

        log_message(
            "Add channel {} video {} to downloaded with episode number {}.".format(
                channel_name, video_id, episode_number
            )
        )

        if not config.pretend:
            sql = "INSERT INTO video (id, episode_number, channel_name) VALUES(?, ?, ?)"
            self._connection.execute(sql, (video_id, episode_number, channel_name))
            self._connection.commit()

    def get_next_episode_number(self, channel_name: str) -> int:
        """Calculate the next episode number from how many episodes we have downloaded

        Args:
            channel_name (str): Channel name (not channel_id)

        Returns:
            int: next episode number
        """
        sql_get_latest_episode = "SELECT episode_number FROM video WHERE channel_name=? ORDER BY episode_number DESC"
        self._cursor.execute(sql_get_latest_episode, [channel_name])
        row = self._cursor.fetchone()
        if row:
            return int(row[0]) + 1
        else:
            return 1

    def has_downloaded(self, video_id: str) -> bool:
        """Check if the video has been downloaded already

        Args:
            video_id (str): YouTube's video id

        Returns:
            bool: True if it has been downloaded, false otherwise
        """
        sql = "SELECT episode_number FROM video WHERE id=?"
        self._cursor.execute(sql, [video_id])
        row = self._cursor.fetchone()
        return bool(row)
