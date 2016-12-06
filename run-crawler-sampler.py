from settings import TELEGRAM_TOKEN, BOT_CHAT_ID, CHECKING_TIMEOUT
from milanuncios_crawler import MilanunciosCrawler
from telegram_writer import TelegramWriter

if __name__ == '__main__':
    bot_1 = MilanunciosCrawler('http://www.milanuncios.com/alquiler-de-viviendas-en-marbella-malaga/?hasta=600&demanda=n&dormd=1')
    bot_2 = MilanunciosCrawler('http://www.milanuncios.com/alquiler-de-viviendas-en-marbella-malaga/?hasta=600&demanda=n&dormd=0')
    telegram = TelegramWriter(TELEGRAM_TOKEN, BOT_CHAT_ID)
    telegram.run([bot_1, bot_2], wait_seconds=CHECKING_TIMEOUT)