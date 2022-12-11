from dataclasses import dataclass
import yaml
import sys
from typing import Optional


@dataclass
class RSS:
    url: str
    download_dir: str
    regex: Optional[str]
    regex_group: Optional[dict]


@dataclass
class Config:
    def __init__(
        self,
        rss_list: list[dict],
        transmission: dict,
        database: dict,
        interval_check_rss: int,
    ):
        self._rss_list = [
            RSS(
                url=rss['url'],
                regex=rss.get('regex'),
                regex_group=rss.get('regex_group'),
                download_dir=rss['download_dir'],
            )
            for rss in rss_list
        ]
        self.transmission = transmission
        self.database = database
        self.interval_check_rss = interval_check_rss

    @staticmethod
    def from_file(file_name: str) -> 'Config':
        with open(file_name, 'r') as stream:
            try:
                config = yaml.safe_load(stream)
                return Config(**config)
            except yaml.YAMLError as exc:
                print(exc)
                sys.exit(1)

    def get_rss(self):
        for rss in self._rss_list:
            yield rss
