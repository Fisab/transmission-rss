import sys

sys.path.append('../src')
from src import filtering


def test_get_series_mapping():
    files = [
        'Shinobi no Ittoki - AniLibria.TV [WEBRip 1080p]/Shinobi_no_Ittoki_[01]_[AniLibria_TV]_[WEBRip_1080p].mkv',
        'Shinobi no Ittoki - AniLibria.TV [WEBRip 1080p]/Shinobi_no_Ittoki_[02]_[AniLibria_TV]_[WEBRip_1080p].mkv',
        'Shinobi no Ittoki - AniLibria.TV [WEBRip 1080p]/Shinobi_no_Ittoki_[200]_[AniLibria_TV]_[WEBRip_1080p].mkv',
    ]

    data = filtering.FeedProcessor.get_series_mapping(files)

    assert list(data.values()) == [1, 2, 200]
