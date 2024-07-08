import discord
from discord import app_commands
from discord.ext import commands

class CreateNewTags(commands.Cog):
    """タグを新規作成"""
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='create_new_tag', description='タグを新規作成します。')
    async def create_new_tag(self, interaction: discord.Interaction, *, tags: str):
        custom_contents = self.bot.get_cog('CustomContents')
        print("create_new_tag")
        tag_list = tags.split()
        tag_dict = {tag: None for tag in tag_list}
        guild = interaction.guild
        print(tag_dict)
        # タグあるか探索
        # ある場合True
        # ない場合False
        """
        タグ検索する処理
        一旦全部True
        """
        for tag in tag_dict:
            tag_dict[tag] = True
        print(tag_dict)
        # タグすべてがある場合
        print(all(tag_dict.values()))
        if all(tag_dict.values()):
            print("is True")
            if custom_contents:
                await custom_contents.send_embed_info(interaction, 'タグリスト', 'すべてのタグが既に存在します。')
            else:
                print("custom_contents cog is not found")
            return
        created_tags = {}
        for tag in tag_dict:
            if tag_dict[tag]:
                continue
            elif not tag_dict[tag]:
                new_channel = await guild.create_text_channel(tag)
                created_tags[tag] = new_channel.id
        if custom_contents:
            await custom_contents.send_embed_info(interaction, 'タグリスト', f'新規作成したタグとチャンネルID:{created_tags}')

async def setup(bot):
    await bot.add_cog(CreateNewTags(bot))