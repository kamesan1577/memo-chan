import discord
from discord import app_commands
from discord.ext import commands

class CreateTags(commands.Cog):
    """タグを新規作成"""
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='create_tag', description='タグを新規作成します。')
    async def create_tag(self, interaction: discord.Interaction, *, tags: str):
        custom_contents = self.bot.get_cog('CustomContents')
        tag_list = tags.split()
        tag_dict = {tag: None for tag in tag_list}
        guild = interaction.guild
        # タグあるか探索
        # ある場合True
        # ない場合False
        """
        タグ検索する処理
        一旦全部False
        """
        for tag in tag_dict:
            tag_dict[tag] = True
        # タグすべてがある場合
            if custom_contents:
                await custom_contents.send_embed_info(interaction, 'タグリスト', 'すべてのタグが既に存在します。')
        created_tags = {}
        for tag in tag_dict:
            if tag_dict[tag] == False:
                new_channel = await guild.create_text_channel(tag)
                created_tags[tag] = new_channel.id
        # メッセージ作成
        if custom_contents:
            created_channels = ' '.join([f"<#{channel_id}>" for channel_id in created_tags.values()])
            await custom_contents.send_embed_info(interaction, 'タグリスト', f'{created_channels} を作成しました。')

async def setup(bot):
    await bot.add_cog(CreateTags(bot))