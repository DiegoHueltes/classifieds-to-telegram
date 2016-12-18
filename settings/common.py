import os

project_dir = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(project_dir, os.pardir, 'posts_n_webs.db')
TEST_DB_PATH = os.path.join(project_dir, os.pardir, 'test_posts_n_webs.db')
TELEGRAM_TOKEN = '<telegram_token>'
BOT_CHAT_ID = '<chat_id>'
SEND_ERRORS_BY_TELEGRAM = False
ERRORS_TELEGRAM_CHAT_ID = BOT_CHAT_ID
CHECKING_TIMEOUT = 60

try:
    from local_settings import *
    print('importing local settings')
except ImportError:
    pass