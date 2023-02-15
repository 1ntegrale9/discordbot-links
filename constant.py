from dotenv import load_dotenv
from os import getenv

load_dotenv()

TOKEN = getenv('DISCORD_BOT_TOKEN')
API_URL = getenv('API_URL')
GAS_URL = getenv('GAS_URL')
LOG_CHANNEL_ID = int(getenv('LOG_CHANNEL_ID', 1068570419528990821))
