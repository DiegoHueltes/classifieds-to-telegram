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
                                time.sleep(3)  # 3 seconds to don't kill the telegram API
                        except RetryAfter as e:
                            # Flood control exceeded. Retry in 175 seconds
                            self.send_error('RetryAfter error, waiting {} seconds'.format(e.retry_after))
                            time.sleep(e.retry_after)
                except Exception:
                    exc_type, exc_value, exc_traceback = sys.exc_info()
                    error_stack = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
                    self.send_error(error_stack)
            time.sleep(wait_seconds)

    def send_error(self, text):
        """
        Sending text using telegram and error channel
        :param text: text to be sent
        """
        try:
            self.telegram.sendMessage(chat_id=settings.ERRORS_TELEGRAM_CHAT_ID, text=text)
        except Exception:
            pass
        print(text)
