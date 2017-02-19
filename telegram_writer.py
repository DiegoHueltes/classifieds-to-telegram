from __future__ import unicode_literals

import datetime
import sys
import traceback
from itertools import groupby

import gevent as gevent
import telegram
from gevent.pool import Pool
from telegram.error import BadRequest, RetryAfter

import settings
from crawlers.crawler_base import Crawler


class TelegramWriter:
    def __init__(self, token, chat_id=None):
        self.telegram = telegram.Bot(token=token)
        self.chat = chat_id
        self.wait_seconds = 60
        self.bots = []
        self.post_chunk = 5

    def posts_fetcher(self):
        while True:
            for bot in self.bots:
                try:
                    if settings.DEBUG:
                        print('Checking for news {} on bot type {}-{}'.format(datetime.datetime.utcnow(), bot.web_type,
                                                                              bot.target_url))
                    chat_id = bot.chat_id or self.chat
                    posts = bot.save_last_updates(chat_id)
                    if settings.DEBUG:
                        print('-- {} New posts saved found'.format(len(posts)))
                except Exception as e:
                    exc_type, exc_value, exc_traceback = sys.exc_info()
                    error_stack = 'Save_updates ERROR: {}\n'.format(e)
                    error_stack += "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
                    self.send_error(error_stack)
            gevent.sleep(self.wait_seconds)

    def telegram_posts_sender(self):
        while True:
            time_to_wait = (self.wait_seconds // 3) + 1
            posts_to_sent = Crawler.get_post_to_send()
            grouped_posts = groupby(posts_to_sent, key=lambda x: x.to_send_id)
            pending_msgs_to_send = False
            for chat_id, posts in grouped_posts:
                pending_msgs_to_send = True
                posts = list(posts)[:self.post_chunk]
                if settings.DEBUG:
                    print('Sending {} new posts to chat {}'.format(len(posts), chat_id))
                for post in posts:
                    try:
                        self.telegram.sendMessage(chat_id=chat_id, text=post.description)
                        if post.image:
                            try:
                                self.telegram.sendPhoto(chat_id=chat_id, photo=post.image)
                            except BadRequest:
                                self.send_error('ERROR sending picture to {}'.format(post))
                        post.status = 'SENT'
                    except RetryAfter as e:
                        # Flood control exceeded. Retry in 175 seconds
                        self.send_error('RetryAfter error, waiting {} seconds'.format(e.retry_after))
                        time_to_wait = max(e.retry_after, time_to_wait)
                        post.status = 'ERROR'
                    except Exception as e:
                        exc_type, exc_value, exc_traceback = sys.exc_info()
                        error_stack = 'Send_updates ERROR: {}\n'.format(e)
                        error_stack += "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
                        self.send_error(error_stack)
                        post.status = 'ERROR'
                Crawler.save_posts(posts)

            if pending_msgs_to_send:
                sleep_time = 3
            else:
                sleep_time = time_to_wait
            gevent.sleep(sleep_time)

    def run(self, bots, wait_seconds=None):
        """
        Setup the bots and seconds to wait and spawn the required gevent
        :param bots: [Crawler]
        :param wait_seconds: seconds for checking the urls
        """
        self.wait_seconds, self.bots = wait_seconds, bots
        pool = Pool()
        pool.spawn(self.posts_fetcher)
        pool.spawn(self.telegram_posts_sender)
        pool.join()

    def send_error(self, text):
        """
        Sending text using telegram and error channel
        :param text: text to be sent
        """
        try:
            self.telegram.sendMessage(chat_id=settings.ERRORS_TELEGRAM_CHAT_ID, text=text)
        except Exception as e:
            print('Error trying to send the error to a ErrorChat {}'.format(e))
        print(text)
