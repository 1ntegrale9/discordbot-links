import discord
from discord.ext import commands
from constant import APPLICATION_ID
from constant import TOKEN

extensions = (
    'url_handle',
)


class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix='$',
            help_command=None,
            intents=discord.Intents.all(),
            application_id=APPLICATION_ID,
        )

    async def setup_hook(self):
        for extension in extensions:
            await self.load_extension(f'extensions.{extension}')
        # await self.tree.sync()


def main():
    MyBot().run(TOKEN)


if __name__ == '__main__':
    main()