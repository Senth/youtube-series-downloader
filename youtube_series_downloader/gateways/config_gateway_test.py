from typing import List

import pytest
from tealprint import TealLevel
from youtube_series_downloader.config import General, config
from youtube_series_downloader.core.channel import Channel
from youtube_series_downloader.gateways.config_gateway import ConfigGateway


@pytest.mark.parametrize(
    "name,config_str,expected",
    [
        (
            "Minimum channel, only an id",
            """
            [Channel Name]
            id = UChFur_NwVSbUozOcF_F2kMf
            """,
            [
                Channel(name="Channel Name", id="UChFur_NwVSbUozOcF_F2kMf"),
            ],
        ),
        (
            "Changing channel name",
            """
            [Channel Name]
            id = UChFur_NwVSbUozOcF_F2kMf
            name = Another name
            """,
            [
                Channel(name="Another name", id="UChFur_NwVSbUozOcF_F2kMf"),
            ],
        ),
        (
            "Collection dir",
            """
            [Channel Name]
            id = UChFur_NwVSbUozOcF_F2kMf
            dir = some/dir
            """,
            [
                Channel(
                    name="Channel Name",
                    id="UChFur_NwVSbUozOcF_F2kMf",
                    collection_dir="some/dir",
                ),
            ],
        ),
        (
            "Speed",
            """
            [Channel Name]
            id = UChFur_NwVSbUozOcF_F2kMf
            speed = 0.8
            """,
            [
                Channel(name="Channel Name", id="UChFur_NwVSbUozOcF_F2kMf", speed=0.8),
            ],
        ),
        (
            "Includes",
            """
            [Channel Name]
            id = UChFur_NwVSbUozOcF_F2kMf
            includes =
                test
                another string
            """,
            [
                Channel(
                    name="Channel Name",
                    id="UChFur_NwVSbUozOcF_F2kMf",
                    includes=["test", "another string"],
                ),
            ],
        ),
        (
            "Excludes",
            """
            [Channel Name]
            id = UChFur_NwVSbUozOcF_F2kMf
            excludes =
                test
                another string
            """,
            [
                Channel(
                    name="Channel Name",
                    id="UChFur_NwVSbUozOcF_F2kMf",
                    excludes=["test", "another string"],
                ),
            ],
        ),
        (
            "Changing channel name",
            """
            [Channel Name]
            id = UChFur_NwVSbUozOcF_F2kMf
            """,
            [
                Channel(name="Channel Name", id="UChFur_NwVSbUozOcF_F2kMf"),
            ],
        ),
    ],
)
def test_get_channels(name: str, config_str: str, expected: List[Channel]) -> None:
    print(name)

    config.general = General()
    gateway = ConfigGateway()
    gateway.parser.read_string(config_str)

    channels = gateway.get_channels()

    assert expected == channels


def test_required_channel_id() -> None:
    gateway = ConfigGateway()
    config_str = """
        [Channel Name]
        name = Another name
    """
    gateway.parser.read_string(config_str)

    with pytest.raises(SystemExit) as e:
        gateway.get_channels()

    assert e.type == SystemExit
    assert e.value.code == 1


def test_get_default_speed() -> None:
    config.general.speed_up_default = 1.5
    gateway = ConfigGateway()
    config_str = """
        [Channel Name]
        id = UChFur_NwVSbUozOcF_F2kMf
    """
    expected = [Channel(name="Channel Name", id="UChFur_NwVSbUozOcF_F2kMf", speed=1.5)]

    gateway.parser.read_string(config_str)

    channels = gateway.get_channels()

    assert expected == channels


def test_required_series_dir() -> None:
    gateway = ConfigGateway()
    config_str = """
        [General]
        serie_dir = invalid/name
    """
    gateway.parser.read_string(config_str)

    with pytest.raises(SystemExit) as e:
        gateway.get_general()

    assert e.type == SystemExit
    assert e.value.code == 1


@pytest.mark.parametrize(
    "level,expected",
    [
        ("none", TealLevel.none),
        ("error", TealLevel.error),
        ("warning", TealLevel.warning),
        ("info", TealLevel.info),
        ("verbose", TealLevel.verbose),
        ("debug", TealLevel.debug),
    ],
)
def test_valid_log_levels(level: str, expected: TealLevel) -> None:
    gateway = ConfigGateway()
    config_str = f"""
        [General]
        series_dir = series
        log_level = {level}
    """

    gateway.parser.read_string(config_str)
    general = gateway.get_general()

    assert expected == general.log_level


def test_invalid_log_level() -> None:
    gateway = ConfigGateway()
    config_str = """
        [General]
        series_dir = series
        log_level = invalid
    """

    gateway.parser.read_string(config_str)
    general = gateway.get_general()

    assert TealLevel.info == general.log_level
