import discord
from discord import app_commands
from discord.ext import commands

class CreateNewTags(commands.Cog):
    """タグを新規作成"""
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='create_new_tag', description='タグを新規作成します。')
    async def create_new_tag(self, interaction: discord.Interaction, *, tags: str):
        tag_list = tags.split()
        # タグリストを表示
        custom_contents = self.bot.get_cog('CustomContents')
        if custom_contents:
            await custom_contents.send_embed_info(interaction, 'タグリスト', f'以下のタグを新規作成します。\n{tag_list}')

async def setup(bot):
    await bot.add_cog(CreateNewTags(bot))