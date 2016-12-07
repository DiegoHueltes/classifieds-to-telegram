import datetime
import time
import traceback

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
                chat_id = self.chat
                try:
                    posts = bot.get()
                    for post in posts:
                        self.telegram.sendMessage(chat_id=chat_id, text=post['text'])
                        if post['image']:
                            self.telegram.sendPhoto(chat_id=chat_id, photo=post['image'])
                except Exception as e:
                    error_text = traceback.print_exc()
                    print(error_text)
                    self.telegram.sendMessage(chat_id=chat_id, text=error_text)
            time.sleep(wait_seconds)
