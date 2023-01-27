import re
from hashlib import sha256
from utils.gas_client import GoogleAppScriptClient


class Text2URL():
    def __init__(self, text):
        self.text: str = text
        self.pattern = r'https?:\/\/[-_.!~*\'()a-zA-Z0-9;\/?:\@&=+\$,%#]+'
        self.domains: dict = {
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
        self.urls: dict = {}
        for url in re.findall(self.pattern, self.text):
            url = url.replace('http://', 'https://')
            domain = url.split('://')[1].split('/')[0]
            site = self.domains.get(domain, 'other')
            self.urls[url] = {
                'domain': domain,
                'site': site,
            }
            if site == 'twitter':
                pattern = re.compile(
                    r'(https?:\/\/twitter\.com\/)([-_.!~*\'()a-zA-Z0-9;\/?:\@&=+\$,%#]+)'
                )
                self.urls[url] |= {'twitter_id': pattern.match(url).group(2).split('/')[0]}


async def save_url(provider, url, data, tags):
    payload = {
        'provider': provider,
        'url': url,
        'tags': ', '.join(tags),
    }
    await GoogleAppScriptClient('all').post(payload)
    for tag in tags:
        payload = {
            'url': url,
            'tags': ', '.join(tags),
        }
        if tag == 'twitter':
            payload |= {'twitter_id': data.get('twitter_id')}
        await GoogleAppScriptClient(tag).post(payload)


def hashing(text: str):
    return sha256(text.encode()).hexdigest()
