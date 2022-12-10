import re


def check_match(title: str, regex: re) -> bool:
	return bool(re.search(regex, title.lower()))


def get_bittorrent_link(links: list, types: list[str] = None):
	if types is None:
		types = [
			'application/x-bittorrent'
		]
	for link in links:
		for type_ in types:
			if link['type'] == type_:
				return link['href']


def get_series_mapping(tv_series: list[str]):
	result = {}
	for name in tv_series:
		search = re.search(r'(\b|_)(\d\d|\d)(\b|_)', name)
		if search:
			result[name] = int(search.group(2))
	return result
