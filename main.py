import discord
from discord.ext import commands
from constant import TOKEN

extensions = (
    'url_handle',
    'gkb',
)

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=commands.when_mentioned,
            help_command=None,
            intents=discord.Intents.all(),
        )

    async def setup_hook(self):
        for extension in extensions:
            await self.load_extension(f'extensions.{extension}')
        await self.tree.sync()

def main():
    MyBot().run(TOKEN)

if __name__ == '__main__':
    main()
