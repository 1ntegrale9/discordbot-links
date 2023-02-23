from dotenv import load_dotenv
from os import getenv

load_dotenv()

TOKEN = getenv('DISCORD_BOT_TOKEN')
API_URL = getenv('API_URL')
GAS_URL = getenv('GAS_URL')
GUILD_LINKS_ID = int(getenv('GUILD_LINKS_ID', 870910390706532382))
LOG_CHANNEL_ID = int(getenv('LOG_CHANNEL_ID', 1068570419528990821))

CHANNEL_TAG_TABLE: dict = {
    '872967889928486912': '人物',
    '872894495430164610': 'イラスト',
    '872841453636841524': '音楽',
    '872940515547578378': '動画',
}

DOMAINS_TABLE: dict = {
    'discord.com': 'discord',
    'ptb.discord.com': 'discord',
    'canary.discord.com': 'discord',
    'twitter.com': 'twitter',
    'open.spotify.com': 'spotify',
    'youtube.com': 'youtube',
    'www.youtube.com': 'youtube',
    'youtu.be': 'youtube',
    'pixiv.net': 'pixiv',
    'www.pixiv.net': 'pixiv',
    'soundcloud.com': 'soundcloud',
    'nicovideo.jp': 'nicovideo',
    'www.nicovideo.jp': 'nicovideo',
}
