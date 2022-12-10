import feedparser
import re
import filtering
import pprint
import requests
from transmission_rpc import Client
from torrentool.api import Torrent
import shelve


url = 'https://api.anilibria.tv/v2/getRSS?rss_type=rss&limit=10'
feeds = feedparser.parse(url)

regex = r'.*время ниндзя.*'


for feed in feeds['entries']:
	if filtering.check_match(feed['title'], regex):
		# print(pprint.pprint(feed))

		torrent_url = filtering.get_bittorrent_link(feed['links'])
		r = requests.get(torrent_url)
		# print(r.status_code, 1488)
		data = Torrent.from_string(r.content)
		print(data.files)
		print(data.files[0].name)
		pprint.pprint(
			filtering.get_series_mapping([f.name for f in data.files])
		)
		# test = c.add_torrent(r.content)
		# print(test, 123)

