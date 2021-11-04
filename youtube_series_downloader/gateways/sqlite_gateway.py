import sqlite3
from pathlib import Path

from tealprint import TealPrint
from youtube_series_downloader.config import config
from youtube_series_downloader.utils.log_colors import LogColors


class SqliteGateway:
    __FILE_PATH = Path.home().joinpath(".youtube-series-downloader.db")

    def __init__(self):
        TealPrint.debug(f"Sqlite DB location: {SqliteGateway.__FILE_PATH}")
        self.__connection = sqlite3.connect(SqliteGateway.__FILE_PATH)
        self.__cursor = self.__connection.cursor()

        # Create DB (if not exists)
        self._create_db()

    def close(self):
        TealPrint.debug("Closing Sqlite DB connection")
        self.__connection.commit()
        self.__connection.close()

    def _create_db(self):
        self.__cursor.execute("Create TABLE IF NOT EXISTS video (id TEXT, episode_number INTEGER, channel_name TEXT)")
        self.__connection.commit()

    def add_downloaded(self, channel_name: str, video_id: str):
        """Adds a downloaded episode to the DB

        Args:
            channel_name (str): Channel name (not channel_id)
            video_id (str): YouTube's video id for the video that was downloaded
        """
        episode_number = self.get_next_episode_number(channel_name)

        TealPrint.debug(
            f"💾 Save to DB {video_id} from {channel_name} with episode number {episode_number}.",
            color=LogColors.added,
        )

        if not config.pretend:
            sql = "INSERT INTO video (id, episode_number, channel_name) VALUES(?, ?, ?)"
            self.__cursor.execute(sql, (video_id, episode_number, channel_name))
            self.__connection.commit()

    def get_next_episode_number(self, channel_name: str) -> int:
        """Calculate the next episode number from how many episodes we have downloaded

        Args:
            channel_name (str): Channel name (not channel_id)

        Returns:
            int: next episode number
        """
        sql_get_latest_episode = "SELECT episode_number FROM video WHERE channel_name=? ORDER BY episode_number DESC"
        self.__cursor.execute(sql_get_latest_episode, [channel_name])
        row = self.__cursor.fetchone()
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
        self.__cursor.execute(sql, [video_id])
        row = self.__cursor.fetchone()
        return bool(row)
