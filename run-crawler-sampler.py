"""
This is another example how to use the crawlers using a list of pairs (url, chat_id) to setup them
"""
from crawlers.milanuncios_crawler import MilanunciosCrawler
from crawlers.vibbo_crawler import VibboCrawler
from settings import TELEGRAM_TOKEN, BOT_CHAT_ID, CHECKING_TIMEOUT
from telegram_writer import TelegramWriter


if __name__ == '__main__':
    bots = []
    # Vibbo example
    url = 'http://www.vibbo.com/portatiles-netbooks-de-segunda-mano-malaga/mac-pro.htm?ca=29_s&fPos=402&fOn=sl1'

    chat_id = '-219998589'  # change for your chat id where your bot can write on
    bots.append(VibboCrawler(url, chat_id))

    # Milanuncios example
    url = 'http://www.milanuncios.com/portatiles-de-segunda-mano-en-malaga/mac-pro.htm'
    bots.append(MilanunciosCrawler(url, chat_id))

    # Instantiating the TelegraWriter with the example crawlers
    telegram = TelegramWriter(TELEGRAM_TOKEN, BOT_CHAT_ID or None)
    telegram.run(bots, wait_seconds=CHECKING_TIMEOUT)
