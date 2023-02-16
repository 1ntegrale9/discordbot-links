import aiohttp
import traceback
import discord
from discord import app_commands
from discord.ext import commands
from constant import API_URL

async def pull(tag: str, send) -> discord.Embed:
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

async def push(tag1: str, tag2: str, send) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.post(f'{API_URL}/push', json={'tag1': tag1, 'tag2': tag2}) as resp:
            if int(resp.status) == 200:
                json = await resp.json()
                values = list(json.values())[0]
                values = '`\n`'.join(values[:10])
                embed = discord.Embed(
                    title=tag1,
                    description=values,
                )
                embed.set_footer(text=f'{tag1} に紐付くタグの一覧')
                await send(embed=embed)
            else:
                json = await resp.json()
                await send(embed=discord.Embed(description='エラーが発生しました'))

class TagModal(discord.ui.Modal, title='2つのテキスト/URLを相互に紐付けて保存'):
    tag1 = discord.ui.TextInput(
        label='テキスト/URL①',
        style=discord.TextStyle.short,
        required=True,
    )

    tag2 = discord.ui.TextInput(
        label='テキスト/URL②',
        style=discord.TextStyle.short,
        placeholder='入力なしで①の検索結果を表示します',
        required=False,
    )

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer()
        if self.tag2.value is None:
            await pull(self.tag1.value, interaction.followup.send)
        else:
            await push(self.tag1.value, self.tag2.value, interaction.followup.send)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('問題が発生しました', ephemeral=True)
        traceback.print_exception(type(error), error, error.__traceback__)

@app_commands.guild_only()
class GraphKnowledgeBaseCog(commands.GroupCog, group_name='辞書'):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='サーバー', description='タグ情報の取得/保存')
    async def guild(self, interaction: discord.Interaction):
        await interaction.response.send_modal(TagModal())

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(GraphKnowledgeBaseCog(bot))
