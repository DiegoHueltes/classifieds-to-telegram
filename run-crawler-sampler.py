"""
This is another example how to use the crawlers using a list of pairs (url, chat_id) to setup them
"""

from settings import TELEGRAM_TOKEN, BOT_CHAT_ID, CHECKING_TIMEOUT, TYPE_URL_N_CHAT
from telegram_writer import TelegramWriter
from crawlers.enalquiler_crawler import EnalquilerCrawler
from crawlers.idealista_crawler import IdealistaCrawler
from crawlers.milanuncios_crawler import MilanunciosCrawler


if __name__ == '__main__':
    bots = []
    crawlers = [('enalquiler', EnalquilerCrawler),
                ('idealista', IdealistaCrawler),
                ('milanuncios', MilanunciosCrawler)]
    for crawler_key, CrawlerInstance in crawlers:
        for url, chat_id in TYPE_URL_N_CHAT[crawler_key]:
            bots.append(CrawlerInstance(url, chat_id))
    telegram = TelegramWriter(TELEGRAM_TOKEN, BOT_CHAT_ID or None)
    telegram.run(bots, wait_seconds=CHECKING_TIMEOUT)
