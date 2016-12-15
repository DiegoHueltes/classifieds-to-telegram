from __future__ import unicode_literals

import datetime
import sys
import time
import traceback

import telegram

import settings


class TelegramWriter:
    def __init__(self, token, chat_id=None):
        self.telegram = telegram.Bot(token=token)
        self.chat = chat_id

    def run(self, bots, wait_seconds):

        while True:
            for bot in bots:
                if settings.DEBUG:
                    print('Checking for news {}'.format(datetime.datetime.utcnow()))
                chat_id = bot.chat_id or self.chat
                try:
                    posts = bot.get_last_updates()
                    for post in posts:
                        self.telegram.sendMessage(chat_id=chat_id, text=post.description)
                        if post.image:
                            self.telegram.sendPhoto(chat_id=chat_id, photo=post.image)
                except Exception as e:
                    exc_type, exc_value, exc_traceback = sys.exc_info()
                    error_stack = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
                    print(error_stack)
                    if settings.SEND_ERRORS_BY_TELEGRAM:
                        try:
                            self.telegram.sendMessage(chat_id=settings.ERRORS_TELEGRAM_CHAT_ID, text=error_stack)
                        except Exception:
                            pass
            time.sleep(wait_seconds)
