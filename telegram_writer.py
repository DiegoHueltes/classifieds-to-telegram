import datetime
import time

import telegram

import settings


class TelegramWriter:
    def __init__(self, token, chat):
        self.telegram = telegram.Bot(token=token)
        self.chat = chat

    def run(self, bots, wait_seconds):

        while True:
            for bot in bots:
                if settings.DEBUG:
                    print('Checking for news {}'.format(datetime.datetime.utcnow()))
                try:
                    posts = bot.get()
                    chat_id = self.chat
                    for post in posts:
                        self.telegram.sendMessage(chat_id=chat_id, text=post['text'])
                        if post['image']:
                            self.telegram.sendPhoto(chat_id=chat_id, photo=post['image'])
                except Exception as e:
                    print(e)
            time.sleep(wait_seconds)
