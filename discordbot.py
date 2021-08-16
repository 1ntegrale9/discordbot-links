from os import getenv
from dotenv import load_dotenv
from discord.ext import commands
import discord

load_dotenv(override=True)

bot = commands.Bot(
    command_prefix=commands.when_mentioned_or('$'),
    help_command=None,
    intents=discord.Intents.all(),
)
bot.load_extension('jishaku')
bot.load_extension('url_extention')
bot.run(getenv('DISCORD_BOT_TOKEN'))
