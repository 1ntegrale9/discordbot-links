from dotenv import load_dotenv
from os import getenv

load_dotenv()

TOKEN = getenv('DISCORD_BOT_TOKEN')
APPLICATION_ID = getenv('APPLICATION_ID', 875837347734900759)
LOG_CHANNEL_ID = int(getenv('LOG_CHANNEL_ID', 1068570419528990821))
