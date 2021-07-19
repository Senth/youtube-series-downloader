import pytest
from youtube_series_downloader.core.channel import Channel
from youtube_series_downloader.gateways.youtube_gateway import YoutubeGateway


@pytest.fixture
def channel() -> Channel:
    return Channel(name="GeminiTay", id="UCUBsjvdHcwZd3ztdY1Zadcw")


@pytest.fixture
def youtube_gateway() -> YoutubeGateway:
    return YoutubeGateway()


def test_get_videos_from_youtube(youtube_gateway: YoutubeGateway, channel: Channel) -> None:
    result = youtube_gateway.get_videos(channel)

    assert len(result) == 15
