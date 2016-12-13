## Classifieds to Telegram library

This is a project for sending classifieds filtered posts updates to a specific Telegram channel
Already supporting updates on milanuncios.com and idealista.com

##Usage
1. Create Python 3.4+ virualenv (mkvirtualenv venv)
2. Install requirements (pip install -r requirements.txt)
3. Create sqllite databases:
```
>>> export PYTHONPATH=.
>>> python db/__init__.py
```
4. Import TelegramWritter and the crawler classes (MilanunciosCrawler or IdealistaCrawler for now)
5. Create a Crawler for every search you want to receive updates
6. Register a Telegram bot and get the token
7. Get the chat_id, you can follow this link to get it https://fullmeter.com/blog/?p=14 or directly use this patter:
  https://api.telegram.org/bot<telegram_token>/getupdates
8. Run TelegramWriter with these crawlers and configure it with the proper token and channel id where you want to receive the updates

Bot example
```python
from settings import TELEGRAM_TOKEN, BOT_CHAT_ID, CHECKING_TIMEOUT
from milanuncios_crawler import MilanunciosCrawler
from telegram_writer import TelegramWriter

if __name__ == '__main__':
    bot_1 = MilanunciosCrawler(here_your_milanuncios_url, chat_id or None)
    bot_2 = MilanunciosCrawler(here_your_second_milanuncios_url, chat_id or None)
    telegram = TelegramWriter(TELEGRAM_TOKEN, BOT_CHAT_ID)
    telegram.run([bot_1, bot_2], wait_seconds=CHECKING_TIMEOUT)
```

As you can see, TelegramWritter.run is designed to receive multiple crawler objects. 

If you want to add some other, you just have to:
* Create a class inereted from __Crawler__ 
* Add the class variables page_type and page_url for the new crawler
* Implement the __get_last_updates__ method returning a list of __Post__ objects


## Instalation in Raspberry Pi or with Python from source
If your system doesn't have python 3.4+ and you are forced to compile it from source (like using a Raspberry Pi) remember to compile it with openssl support to install pip and sqlite support:
* sudo apt-get install libssl-dev openssl libsqlite3-dev
* ./configure --enable-loadable-sqlite-extensions --with-ensurepip=install && make && make install

##TODO:
1. Add some doc to the functions
2. Create other crawlers ~~(for instance idealista crawler)~ (for instance fotocasa)
3. Make it reactive to bot interactions (so, make it a real bot). Some useful custom actions would be to add new urls to track