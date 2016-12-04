import telegram
import time


class TelegramWriter:
    def __init__(self, token, chat):
        self.telegram = telegram.Bot(token=token)
        self.chat = chat

    def run(self, bots, wait_seconds):

        while True:
            for bot in bots:
                try:
                    posts = bot.get()
                    for post in posts:
                        self.telegram.sendMessage(chat_id=self.chat, text=post['text'])
                        if post['image']:
                            self.telegram.sendPhoto(chat_id=self.chat, photo=post['image'])
                except Exception as e:
                    print(e)
            time.sleep(wait_seconds)
