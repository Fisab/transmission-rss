import feedparser
import filtering
import requests
from transmission_rpc import Client
from torrentool.api import Torrent
from config_parser import Config
from database import DatabaseClient
import logging
from time import sleep


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


def main(config: Config, transmission_client: Client, db_client: DatabaseClient):
    for rss in config.get_rss():
        logger.info(f'Processing rss with url: {rss.url}')
        feeds = feedparser.parse(rss.url)

        for feed in feeds['entries']:
            # TODO: добавить обработку если rss.regex - None
            # TODO: добавить работу с группами регулряок - rss.regex_group
            logger.debug(f'Got feed with title {feed["title"]}')
            feed_processor = filtering.FeedProcessor(feed['title'], rss, db_client)
            feed_match = feed_processor.check_match()

            if not feed_match:
                logger.debug('Feed skipped')
                continue

            torrent_url = feed_processor.get_bittorrent_link(feed['links'])
            r = requests.get(torrent_url)
            torrent = Torrent.from_string(r.content)  # noqa
            feed_processor.update_torrents_files_to_download(torrent)
            logger.info(
                f'For feed "{feed["title"]}" got {len(feed_processor.to_downloads)} files to download'
            )

            if feed_processor.to_downloads:
                transmission_client.add_torrent(
                    r.content,
                    files_wanted=feed_processor.to_downloads,
                    download_dir=rss.download_dir,
                    paused=False,
                )
                logger.info('Successfully added to transmission')
                db_client.remember_series_name(
                    name=feed['title'], series=feed_processor.get_to_download_series()
                )


if __name__ == '__main__':
    config_ = Config.from_file('./config.yml')
    logger.info('Loaded config')
    db_client_ = DatabaseClient(file_name=config_.database.get('file_name'))
    transmission_client_ = Client(**config_.transmission)

    while True:
        try:
            main(config_, transmission_client_, db_client_)
            sleep(config_.interval_check_rss)
        except Exception as ex:
            logger.error(f'Got error when processing: {ex}')
            logger.error(f'Waiting {sleep(config_.interval_check_rss)} seconds...')
            sleep(config_.interval_check_rss)

    # TODO: нужен механизм для извлечения торрентов
    #  и обновления в бд, которые добавили вручную
