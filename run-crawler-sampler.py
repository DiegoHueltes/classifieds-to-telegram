"""
This is another example how to use the crawlers using a list of pairs (url, chat_id) to setup them
"""
from crawlers.idealista_crawler import IdealistaCrawler
from crawlers.milanuncios_crawler import MilanunciosCrawler
from settings import TELEGRAM_TOKEN, BOT_CHAT_ID, CHECKING_TIMEOUT, MILANUNCIOS_URL_N_CHAT, IDEALISTA_URL_N_CHAT
from telegram_writer import TelegramWriter

if __name__ == '__main__':
    bots = []
    for url, chat_id in MILANUNCIOS_URL_N_CHAT:
        bots.append(MilanunciosCrawler(url, chat_id))
    for url, chat_id in IDEALISTA_URL_N_CHAT:
        bots.append(IdealistaCrawler(url, chat_id))
    telegram = TelegramWriter(TELEGRAM_TOKEN, BOT_CHAT_ID or None)
    telegram.run(bots, wait_seconds=CHECKING_TIMEOUT)
