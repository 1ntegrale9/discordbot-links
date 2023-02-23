import re
from hashlib import sha256
from utils import gas_client
from constant import GAS_URL
from constant import DOMAINS_TABLE

REGEXP_URL = r'https?:\/\/[-_.!~*\'()a-zA-Z0-9;\/?:\@&=+\$,%#]+'
REGEXP_URL_TWITTER = r'(https?:\/\/twitter\.com\/)([-_.!~*\'()a-zA-Z0-9;\/?:\@&=+\$,%#]+)'
PATTERN_TWITTER = re.compile(REGEXP_URL_TWITTER)

def get_urls_from_text(text: str):
    urls: dict = {}
    for url in re.findall(REGEXP_URL, text):
        url = url.replace('http://', 'https://')
        domain = url.split('://')[1].split('/')[0]
        site = DOMAINS_TABLE.get(domain, 'other')
        urls[url] = {
            'domain': domain,
            'site': site,
        }
        if site == 'twitter':
            urls[url] |= {'twitter_id': PATTERN_TWITTER.match(url).group(2).split('/')[0]}
    return urls

async def save_url(provider, url, data, tags):
    payload = {
        'provider': provider,
        'url': url,
        'tags': ', '.join(tags),
    }
    await gas_client.post(GAS_URL, 'all', payload)
    for tag in tags:
        payload = {
            'url': url,
            'tags': ', '.join(tags),
        }
        if tag == 'twitter':
            payload |= {'twitter_id': data.get('twitter_id')}
        await gas_client.post(GAS_URL, tag, payload)

def hashing(text: str):
    return sha256(text.encode()).hexdigest()
