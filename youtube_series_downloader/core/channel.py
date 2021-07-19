from typing import List

from youtube_series_downloader.config import config


class Channel:
    def __init__(
        self,
        name: str = "",
        id: str = "",
        collection_dir: str = "",
        speed: float = config.general.speed_up_default,
        includes: List[str] = [],
        excludes: List[str] = [],
    ):
        self.name = name
        self.id = id
        self.collection_dir = collection_dir
        self.speed = speed
        self.includes = includes
        self.excludes = excludes

    # def get_videos(self) -> List[Video]:
    #     TealPrint.info(self.name, color=LogColors.header)

    #     url = Channel._RSS_PREFIX + self.id
    #     xml = requests.get(url).text

    #     matches = Channel._REGEX.findall(xml)
    #     matches.reverse()

    #     videos = []

    #     for groups in matches:
    #         id = groups[0]
    #         title = groups[1]
    #         date = groups[2]
    #         TealPrint.verbose(
    #             f"🔎 Checking video {id} {colored.attr('bold')}{title}{colored.attr('reset')} — {date}", indent=1
    #         )

    #         if self._is_new(date) and self._matches_includes(title) and not self._matches_excludes(title):
    #             video = Video(id, date, title)
    #             TealPrint.info(f"➕ {title}", color=LogColors.added, indent=1)
    #             videos.append(video)

    #     return videos

    # def _is_new(self, dateString: str) -> bool:
    #     # If config is set to 0. All episodes are new
    #     if config.max_days_back == 0:
    #         return True
    #     else:
    #         date = datetime.strptime(dateString, "%Y-%m-%dT%H:%M:%S%z")
    #         diff_time = datetime.now() - date.replace(tzinfo=None)

    #         if diff_time.days <= config.max_days_back:
    #             TealPrint.verbose(f"🟢 New by {diff_time.days} days", color=LogColors.passed, indent=2)
    #             return True
    #         else:
    #             TealPrint.verbose(f"🔴 Old by {diff_time.days} days", color=LogColors.skipped, indent=2)
    #             return False

    # def matches_excludes(self, title: str) -> bool:
    #     for filter in self.excludes:
    #         if re.search(filter, title):
    #             TealPrint.verbose(f"🔴 Exclude: {filter}", color=LogColors.skipped, indent=2)
    #             return True

    #     TealPrint.verbose("🟢 No matching excludes", color=LogColors.passed, indent=2)
    #     return False

    # def matches_includes(self, title: str) -> bool:
    #     if len(self.includes) == 0:
    #         return True

    #     for filter in self.includes:
    #         if re.search(filter, title):
    #             TealPrint.verbose(f"🟢 Include: {filter}", color=LogColors.passed, indent=2)
    #             return True

    #     TealPrint.verbose("🔴 No matching includes", color=LogColors.skipped, indent=2)
    #     return False
