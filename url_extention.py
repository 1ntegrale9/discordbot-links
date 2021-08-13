from Daug.functions import excepter
from discord import Message
from discord.ext import commands
from gas_client import GoogleAppScriptClient
from hashlib import sha256
import re


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


class UrlHandleCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.guild_id = 870910390706532382
        self.channels = {
            '872967889928486912': '人物',
            '872894495430164610': 'イラスト',
            '872841453636841524': '音楽',
            '872940515547578378': '動画',
        }

    @commands.Cog.listener()
    @excepter
    async def on_message(self, message: Message):
        if message.guild is None:
            return
        if message.guild.id != self.guild_id:
            return
        provider = hashing(str(message.author.id))
        text2url = Text2URL(message.content)
        if len(text2url.urls) == 0:
            return
        save_count = 0
        for url, data in text2url.urls.items():
            if data.get('site') == 'discord':
                continue
            await save_url(
                provider,
                url,
                data,
                {data.get('site'), self.channels.get(str(message.channel.id))} - {None},
            )
            save_count += 1
        if save_count > 0:
            await message.add_reaction('💾')


def hashing(text: str):
    return sha256(text.encode()).hexdigest()


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


def setup(bot):
    bot.add_cog(UrlHandleCog(bot))
