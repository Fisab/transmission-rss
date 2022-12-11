import re
from config_parser import RSS
from torrentool.api import Torrent
from database import DatabaseClient
import logging


logger = logging.getLogger(__name__)


class FeedProcessor:
    def __init__(self, feed_title: str, rss: RSS, db_client: DatabaseClient):
        self._rss = rss
        self._db_client = db_client

        self.feed_title = feed_title
        self.to_downloads = []
        self.series_mapping = {}

    def check_match(self) -> bool:
        if self._rss.regex_group:
            must_mapping = {r: False for r in self._rss.regex_group.get('must', [])}
            must_not_mapping = {
                r: False for r in self._rss.regex_group.get('must_not', [])
            }
            for regex in must_mapping:
                must_mapping[regex] = self._check_match_bool(self.feed_title, regex)
            for regex in must_not_mapping:
                must_not_mapping[regex] = not self._check_match_bool(
                    self.feed_title, regex
                )
            must_match = sum(must_mapping.values()) == len(must_mapping.values())
            must_not_match = sum(must_not_mapping.values()) == len(
                must_not_mapping.values()
            )

            return must_match and must_not_match

        # TODO: релаизовать поддержку одиночного regex

    def get_to_download_series(self):
        return [
            self.series_mapping[name]
            for name in self.series_mapping
            if name in self.to_downloads
        ]

    def update_torrents_files_to_download(self, torrent: Torrent):
        self.series_mapping = self.get_series_mapping([f.name for f in torrent.files])
        seen_series = self._db_client.get_series_by_name(self.feed_title)
        self.to_downloads = [
            file_name
            for file_name in self.series_mapping
            if self.series_mapping[file_name] not in seen_series
        ]

    @staticmethod
    def _check_match_bool(string: str, regex: str):
        return bool(re.search(regex, string.lower()))

    @staticmethod
    def get_series_mapping(tv_series: list[str]):
        result = {}
        for name in tv_series:
            search = re.search(r'(\[|\b|_)(\d+)(\]|\b|_)', name)
            if search:
                result[name] = int(search.group(2))
        return result

    @staticmethod
    def get_bittorrent_link(links: list, types: list[str] = None):
        if types is None:
            types = ['application/x-bittorrent']
        for link in links:
            for type_ in types:
                if link['type'] == type_:
                    return link['href']
