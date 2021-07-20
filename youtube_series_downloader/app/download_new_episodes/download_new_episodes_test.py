from datetime import datetime, timedelta, timezone, tzinfo
from pathlib import Path
from typing import List, Literal, Optional, Set, Union

import pytest
from mockito import mock, unstub, verifyStubbedInvocationsAreUsed, when
from youtube_series_downloader.app.download_new_episodes.download_new_episodes import (
    DownloadNewEpisodes,
)
from youtube_series_downloader.app.download_new_episodes.download_new_episodes_repo import (
    DownloadNewEpisodesRepo,
)
from youtube_series_downloader.config import config
from youtube_series_downloader.core.channel import Channel
from youtube_series_downloader.core.video import Video


@pytest.fixture
def repo():
    return mock(DownloadNewEpisodesRepo)


def case_input(
    name: str,
    includes: List[str] = [],
    excludes: List[str] = [],
    videos: List[Video] = [],
    after_filtered: Optional[List[Video]] = None,
    has_downloaded: Set[str] = set(),
    downloaded_path: Union[Optional[Path], Literal[False]] = Path(""),
    rendered: Optional[bool] = True,
):
    if after_filtered is None:
        after_filtered = videos
    return (name, includes, excludes, videos, after_filtered, has_downloaded, downloaded_path, rendered)


def video(id: str = "id", days_from_today: int = 0, title: str = "title") -> Video:
    now = datetime.now().astimezone() - timedelta(days=days_from_today)
    date_string = now.strftime("%Y-%m-%dT%H:%M:%S%z")
    return Video(id, date_string, title)


@pytest.mark.parametrize(
    "name,includes,excludes,videos,after_filtered,has_downloaded,downloaded_path,rendered",
    [
        case_input(
            name="do nothing when there's no videos",
            downloaded_path=False,
            rendered=None,
        ),
        case_input(
            name="work in the minimal case",
            videos=[video()],
        ),
        case_input(
            name="only include videos from includes",
            includes=["kongo"],
            videos=[
                video(title="kongo episode 01"),
                video(title="be excluded"),
            ],
            after_filtered=[
                video(title="kongo episode 01"),
            ],
        ),
        case_input(
            name="only include videos when includes has capital letters",
            includes=["KONGO"],
            videos=[
                video(title="kongo episode 01"),
                video(title="KONGO episode 02 - Stuff"),
                video(title="be excluded"),
                video(title="also Kongo"),
            ],
            after_filtered=[
                video(title="kongo episode 01"),
                video(title="KONGO episode 02 - Stuff"),
                video(title="also Kongo"),
            ],
        ),
        case_input(
            name="only include videos when includes has non-capital letters",
            includes=["kongo"],
            videos=[
                video(title="kongo episode 01"),
                video(title="KONGO episode 02 - Stuff"),
                video(title="be excluded"),
                video(title="also Kongo"),
            ],
            after_filtered=[
                video(title="kongo episode 01"),
                video(title="KONGO episode 02 - Stuff"),
                video(title="also Kongo"),
            ],
        ),
        case_input(
            name="only include videos when matching any include",
            includes=["kongo", "australia"],
            videos=[
                video(title="kongo episode 01"),
                video(title="be excluded"),
                video(title="also Kongo"),
                video(title="kangaroos in australia"),
                video(title="no kangaroos in austria"),
            ],
            after_filtered=[
                video(title="kongo episode 01"),
                video(title="also Kongo"),
                video(title="kangaroos in australia"),
            ],
        ),
        case_input(
            name="excludes videos from exclude",
            excludes=["kongo"],
            videos=[
                video(title="kongo episode 01"),
                video(title="be included"),
            ],
            after_filtered=[
                video(title="be included"),
            ],
        ),
        case_input(
            name="exclude all videos from exclude (capital letters)",
            excludes=["KONGO"],
            videos=[
                video(title="kongo episode 01"),
                video(title="KONGO episode 02 - Stuff"),
                video(title="be included"),
                video(title="also Kongo"),
            ],
            after_filtered=[
                video(title="be included"),
            ],
        ),
        case_input(
            name="exclude all videos from exclude (non-capital letters)",
            excludes=["kongo"],
            videos=[
                video(title="kongo episode 01"),
                video(title="KONGO episode 02 - Stuff"),
                video(title="be included"),
                video(title="also Kongo"),
            ],
            after_filtered=[
                video(title="be included"),
            ],
        ),
        case_input(
            name="exclude all from exclude (multiple filters)",
            excludes=["kongo", "australia"],
            videos=[
                video(title="kongo episode 01"),
                video(title="be included"),
                video(title="also Kongo"),
                video(title="kangaroos in australia"),
                video(title="no kangaroos in austria"),
            ],
            after_filtered=[
                video(title="be included"),
                video(title="no kangaroos in austria"),
            ],
        ),
        case_input(
            name="pass the filter when matching any include and no excludes",
            includes=["kongo", "australia"],
            excludes=["kangaroo"],
            videos=[
                video(title="kongo episode 01"),
                video(title="be excluded"),
                video(title="kongo doesn't have kangaroos"),
                video(title="australia has kangaroos"),
                video(title="austria is another country"),
                video(title="australia is a large country"),
            ],
            after_filtered=[
                video(title="kongo episode 01"),
                video(title="australia is a large country"),
            ],
        ),
        case_input(
            name="Regex include",
            includes=[r"ship e\d{1,2} -"],
            videos=[
                video(title="ship e01 - something"),
                video(title="ship e100 - not included"),
                video(title="This is a great episod, ship e99 - The greatest"),
            ],
            after_filtered=[
                video(title="ship e01 - something"),
                video(title="This is a great episod, ship e99 - The greatest"),
            ],
        ),
        case_input(
            name="filter out by date",
            # max_days_back = 10, just for testing
            videos=[
                video(title="new", days_from_today=0),
                video(title="old", days_from_today=20),
                video(title="new", days_from_today=5),
                video(title="old", days_from_today=10),
                video(title="old", days_from_today=11),
                video(title="new", days_from_today=9),
            ],
            after_filtered=[
                video(title="new", days_from_today=0),
                video(title="new", days_from_today=5),
                video(title="new", days_from_today=9),
            ],
        ),
    ],
)
def test_download_new_episodes(
    name: str,
    includes: List[str],
    excludes: List[str],
    videos: List[Video],
    after_filtered: List[Video],
    has_downloaded: Set[str],
    downloaded_path: Optional[Path],
    rendered: Optional[bool],
    repo: DownloadNewEpisodesRepo,
):
    print(name)

    config.general.max_days_back = 10

    when(repo).get_latest_videos(...).thenReturn(videos)

    # Default has_downloaded to false if not specified otherwise
    if len(videos) > len(has_downloaded):
        when(repo).has_downloaded(...).thenReturn(False)

    for video in has_downloaded:
        when(repo).has_downloaded(video).thenReturn(True)

    if downloaded_path is not False:
        for video in after_filtered:
            when(repo).download(video).thenReturn(downloaded_path)
        when(repo).get_next_episode_number(...).thenReturn(1)

    if rendered is not None:
        when(repo).render(...).thenReturn(rendered)

    if rendered is True:
        when(repo).set_as_downloaded(...)

    case = DownloadNewEpisodes(repo)
    channels: List[Channel] = [Channel(includes=includes, excludes=excludes)]

    case.execute(channels)

    verifyStubbedInvocationsAreUsed()
    unstub()
