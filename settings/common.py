TELEGRAM_TOKEN = '<telegram_token>'
BOT_CHAT_ID = '<chat_id>'
CHECKING_TIMEOUT = 60

try:
    from local_settings import *
    print('importing local settings')
except ImportError:
    pass