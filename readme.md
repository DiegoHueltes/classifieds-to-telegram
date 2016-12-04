## Classifieds to Telegram library

This is a project for sending classifieds filtered posts updates to a specific Telegram channel
The first integration is milanuncios.com

##Usage
1. Create Python 3 virualenv (mkvirtualenv venv)
2. Install requirements (pip install -r requirements.txt)
3. Create sqllite databases (python init_db.py)
3. Import TelegramWritter and the crawler classes (MilanunciosCrawler for now)
4. Create a MilanunciosCrawler for every search you want to receive updates
5. Register a Telegram bot and get the token
6. Run TelegramWriter with these crawlers and configure it with the proper token and channel id where you want to receive the updates

Bot example
```python`
from milanuncios_crawler import MilanunciosCrawler
from telegram_writer import TelegramWriter

if __name__ == '__main__':
    bot_1 = MilanunciosCrawler(here_your_milanuncios_url)
    bot_2 = MilanunciosCrawler(here_your_second_milanuncios_url)
    telegram = TelegramWriter(here_your_telegram_bot_token, here_your_channel_id)
    telegram.run([bot_1, bot_2], wait_seconds=60)
``

As you can see, TelegramWritter.run is designed to receive multiple crawler objects. 
If you want to add some other, you just have to create a class with a method "get" that returns a strings list with the messages to send

##TODO:
1. Add some doc to the functions
2. Create other crawlers (for instance idealista crawler)
3. Make it reactive to bot interactions (so, make it a real bot). Some useful custom actions would be to add new urls to track