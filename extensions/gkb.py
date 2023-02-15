import aiohttp
import traceback
import discord
from discord import app_commands
from discord.ext import commands
from constant import API_URL

async def get(tag: str, send) -> discord.Embed:
    async with aiohttp.ClientSession() as session:
        async with session.post(f'{API_URL}/pull', json={'tag': tag}) as resp:
            if int(resp.status) == 200:
                result = await resp.json()
                values = '`\n`'.join(result[:10])
                embed = discord.Embed(
                    title=tag,
                    description=values or 'None',
                )
                embed.set_footer(text=f'{tag} に紐付くタグの一覧')
                await send(embed=embed)
            else:
                json = await resp.json()
                await send(embed=discord.Embed(description='エラーが発生しました'))

async def save(tag: str, text: str, send) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.post(f'{API_URL}/push', json={'tag1': tag, 'tag2': text}) as resp:
            if int(resp.status) == 200:
                json = await resp.json()
                values = list(json.values())[0]
                values = '`\n`'.join(values[:10])
                embed = discord.Embed(
                    title=tag,
                    description=values,
                )
                embed.set_footer(text=f'{tag} に紐付くタグの一覧')
                await send(embed=embed)
            else:
                json = await resp.json()
                await send(embed=discord.Embed(description='エラーが発生しました'))

class GetModal(discord.ui.Modal, title='タグに紐付くテキスト情報の取得'):
    tag = discord.ui.TextInput(
        label='タグ',
        style=discord.TextStyle.short,
    )

    async def on_submit(self, interaction: discord.Interaction):
        await get(self.tag.value, interaction.response.send_message)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('問題が発生しました', ephemeral=True)
        traceback.print_exception(type(error), error, error.__traceback__)

class SaveModal(discord.ui.Modal, title='タグにテキスト/URLを紐付けて保存'):
    text1 = discord.ui.TextInput(
        label='テキスト/URL',
        style=discord.TextStyle.short,
    )

    text2 = discord.ui.TextInput(
        label='テキスト/URL',
        style=discord.TextStyle.short,
    )

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer()
        await save(self.text1.value, self.text2.value, interaction.followup.send)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('問題が発生しました', ephemeral=True)
        traceback.print_exception(type(error), error, error.__traceback__)

class GraphKnowledgeBaseCog(commands.GroupCog, group_name='tag'):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='get', description='タグ情報の取得')
    async def get(self, interaction: discord.Interaction, tag: str = ''):
        if tag == '':
            await interaction.response.send_modal(GetModal())
        else:
            await interaction.response.defer()
            await get(tag, interaction.followup.send)

    @app_commands.command(name='save', description='タグ情報の送信')
    @app_commands.describe(tag='タグ', text='タグに紐付ける文字列/URL')
    @app_commands.rename(tag='タグ', text='文字列またはurl')
    async def save(self, interaction: discord.Interaction, tag: str = '', text: str = ''):
        if tag == '' or text == '':
            await interaction.response.send_modal(SaveModal())
        else:
            await interaction.response.defer()
            await save(tag, text, interaction.followup.send)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(GraphKnowledgeBaseCog(bot))
