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
6. Get the chat_id, you can follow this link to get it https://fullmeter.com/blog/?p=14 or directly use this patter:
  https://api.telegram.org/bot<telegram_token>/getupdates
7. Run TelegramWriter with these crawlers and configure it with the proper token and channel id where you want to receive the updates

Bot example
```python
from settings import TELEGRAM_TOKEN, BOT_CHAT_ID, CHECKING_TIMEOUT
from milanuncios_crawler import MilanunciosCrawler
from telegram_writer import TelegramWriter

if __name__ == '__main__':
    bot_1 = MilanunciosCrawler(here_your_milanuncios_url)
    bot_2 = MilanunciosCrawler(here_your_second_milanuncios_url)
    telegram = TelegramWriter(TELEGRAM_TOKEN, BOT_CHAT_ID)
    telegram.run([bot_1, bot_2], wait_seconds=CHECKING_TIMEOUT)
```

As you can see, TelegramWritter.run is designed to receive multiple crawler objects. 
If you want to add some other, you just have to create a class with a method "get" that returns a list with the messages and photos to send in this format:
```python
{'image': image_url, 'text': text_to_send}
```

##TODO:
1. Add some doc to the functions
2. Create other crawlers (for instance idealista crawler)
3. Make it reactive to bot interactions (so, make it a real bot). Some useful custom actions would be to add new urls to track