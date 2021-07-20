import re
from typing import List

import requests
from youtube_series_downloader.core.channel import Channel
from youtube_series_downloader.core.video import Video


class YoutubeGateway:
    __RSS_PREFX: str = "https://www.youtube.com/feeds/videos.xml?channel_id="
    __REGEX = re.compile(
        r"<entry>.*?<yt:videoId>(.*?)<\/yt:videoId>.*?<title>(.*?)<\/title>.*?<published>(.*?)<\/published>.*?<\/entry>",
        re.DOTALL,
    )

    @staticmethod
    def get_videos(channel: Channel) -> List[Video]:
        url = YoutubeGateway.__RSS_PREFX + channel.id
        xml = requests.get(url).text

        matches = YoutubeGateway.__REGEX.findall(xml)
        matches.reverse()

        videos = []

        for groups in matches:
            id = groups[0]
            title = groups[1]
            date = groups[2]
            video = Video(id, date, title)
            videos.append(video)

        return videos
