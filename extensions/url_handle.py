from discord import Message
from discord.ext import commands
from utils import Text2URL
from utils import save_url
from utils import hashing
from utils.dpyexcept import excepter

GUILD_LINKS_ID = 870910390706532382

class UrlHandleCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
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
        if message.guild.id != GUILD_LINKS_ID:
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

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(UrlHandleCog(bot))
