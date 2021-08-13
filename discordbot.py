from os import getenv
from discord.ext import commands
import discord


bot = commands.Bot(
    command_prefix=commands.when_mentioned_or('$'),
    help_command=None,
    intents=discord.Intents.all(),
)
bot.load_extension('jishaku')
bot.load_extension('url_extention')
bot.run(getenv('DISCORD_BOT_TOKEN'))

