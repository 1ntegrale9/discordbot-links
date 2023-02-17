import aiohttp
import traceback
import discord
from discord import app_commands
from discord.ext import commands
from constant import API_URL

async def pull(tag: str, domain: str, domain_id: str, user_id: str, send) -> discord.Embed:
    URL = f'{API_URL}/pull'
    payload = {'tag': tag, 'domain': domain, 'domain_id': domain_id, 'user_id': user_id}
    async with aiohttp.ClientSession() as session:
        async with session.post(URL, json=payload) as resp:
            if int(resp.status) == 200:
                result = await resp.json()
                values = '\n'.join(result[:10])
                embed = discord.Embed(
                    title=tag,
                    description=values or '検索結果なし',
                )
                embed.set_footer(text=f'{tag} に紐付くテキスト情報/URL一覧')
                await send(embed=embed)
            else:
                await send(embed=discord.Embed(description='エラーが発生しました'), ephemeral=True)

async def push(tag1: str, tag2: str, domain: str, domain_id: str, user_id: str, send) -> str:
    URL = f'{API_URL}/push'
    payload = {'tag1': tag1, 'tag2': tag2, 'domain': domain, 'domain_id': domain_id, 'user_id': user_id}
    async with aiohttp.ClientSession() as session:
        async with session.post(URL, json=payload) as resp:
            if int(resp.status) == 200:
                value1, value2 = await resp.json()
                embed1 = discord.Embed(
                    title=tag1,
                    description='\n'.join(value1),
                )
                embed1.set_footer(text=f'{tag1} に紐付くテキスト情報/URL一覧')
                embed2 = discord.Embed(
                    title=tag2,
                    description='\n'.join(value2),
                )
                embed2.set_footer(text=f'{tag2} に紐付くテキスト情報/URL一覧')
                await send(embeds=[embed1, embed2])
            else:
                await send(embed=discord.Embed(description='エラーが発生しました'), ephemeral=True)

class TagModal(discord.ui.Modal, title='辞書情報の取得または保存'):
    def __init__(self, domain: str, domain_id: str, user_id: str):
        super().__init__()
        self.domain = domain
        self.domain_id = domain_id
        self.user_id = user_id

    tag1 = discord.ui.TextInput(
        label='テキスト/URL①',
        style=discord.TextStyle.short,
        placeholder='保存または検索したいテキストを入力',
        required=True,
    )

    tag2 = discord.ui.TextInput(
        label='テキスト/URL②',
        style=discord.TextStyle.short,
        placeholder='①に紐付けるテキストを入力（入力なしで①を検索）',
        required=False,
    )

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer()
        if self.tag2.value == '':
            await pull(self.tag1.value, self.domain, self.domain_id, self.user_id, interaction.followup.send)
        else:
            await push(self.tag1.value, self.tag2.value, self.domain, self.domain_id, self.user_id, interaction.followup.send)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('エラーが発生しました', ephemeral=True)
        traceback.print_exception(type(error), error, error.__traceback__)

class GraphKnowledgeBaseCog(commands.GroupCog, group_name='辞書'):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='全体共有', description='辞書情報の取得/保存')
    async def global_dictionary(self, interaction: discord.Interaction):
        modal = TagModal(
            domain='',
            domain_id='',
            user_id=f'discord_user_{interaction.user.id}',
        )
        await interaction.response.send_modal(modal)

    @app_commands.guild_only()
    @app_commands.command(name='サーバー専用', description='サーバー専用辞書情報の取得/保存')
    async def guild_dictionary(self, interaction: discord.Interaction):
        modal = TagModal(
            domain='discord',
            domain_id=f'discord_guild_{interaction.guild.id}',
            user_id=f'discord_user_{interaction.user.id}',
        )
        await interaction.response.send_modal(modal)

    @app_commands.command(name='個人専用', description='個人専用辞書情報の取得/保存')
    async def private_dictionary(self, interaction: discord.Interaction):
        modal = TagModal(
            domain='discord',
            domain_id=f'discord_user_{interaction.user.id}',
            user_id=f'discord_user_{interaction.user.id}',
        )
        await interaction.response.send_modal(modal)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(GraphKnowledgeBaseCog(bot))
