from __future__ import unicode_literals

import datetime
import sys
import time
import traceback

import telegram
from telegram.error import BadRequest, RetryAfter

import settings


class TelegramWriter:
    def __init__(self, token, chat_id=None):
        self.telegram = telegram.Bot(token=token)
        self.chat = chat_id

    def run(self, bots, wait_seconds):

        while True:
            print('\nStarting a bunch of checks {}'.format(datetime.datetime.utcnow()))
            for bot in bots:
                if settings.DEBUG:
                    print('Checking for news {} on bot type {}-{}'.format(datetime.datetime.utcnow(), bot.web_type,
                                                                          bot.target_url))
                chat_id = bot.chat_id or self.chat
                try:
                    posts = bot.get_last_updates()
                    if settings.DEBUG:
                        print('-- {} New posts found'.format(len(posts)))
                    for post in posts:
                        try:
                            self.telegram.sendMessage(chat_id=chat_id, text=post.description)
                            if post.image:
                                try:
                                    self.telegram.sendPhoto(chat_id=chat_id, photo=post.image)
                                except BadRequest:
                                    pass
                            if len(posts):
                                time.sleep(5)  # 5 seconds to don't kill the telegram API
                        except RetryAfter as e:
                            # Flood control exceeded. Retry in 175 seconds
                            time.sleep(175)
                except Exception as e:
                    exc_type, exc_value, exc_traceback = sys.exc_info()
                    error_stack = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
                    if settings.SEND_ERRORS_BY_TELEGRAM:
                        try:
                            self.telegram.sendMessage(chat_id=settings.ERRORS_TELEGRAM_CHAT_ID, text=error_stack)
                        except Exception:
                            pass
                    print(error_stack)
            time.sleep(wait_seconds)
