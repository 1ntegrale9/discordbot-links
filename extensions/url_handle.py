from discord import Message
from discord.ext import commands
from utils import get_urls_from_text
from utils import save_url
from utils import hashing
from utils.dpyexcept import excepter
from constant import GUILD_LINKS_ID
from constant import CHANNEL_TAG_TABLE

class UrlHandleCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    @excepter
    async def on_message(self, message: Message):
        if message.guild is None:
            return
        if message.guild.id != GUILD_LINKS_ID:
            return
        provider = hashing(str(message.author.id))
        urls = get_urls_from_text(message.content)
        if len(urls) == 0:
            return
        channel_tag = CHANNEL_TAG_TABLE.get(str(message.channel.id))
        is_saved = False
        for url, data in urls.items():
            if data.get('site') == 'discord':
                continue
            tags = {data.get('site'), channel_tag} - {None}
            await save_url(provider, url, data, tags)
            is_saved = True
        if is_saved:
            await message.add_reaction('💾')

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(UrlHandleCog(bot))
