import discord
from discord import app_commands
from discord.ext import commands
from discord_memo.db.database import SessionLocal

from .utils import create_tag_and_channel

class CreateTags(commands.Cog):
    """タグを新規作成"""
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='create_tag', description='タグを新規作成します。')
    async def create_tag(self, interaction: discord.Interaction, *, tags: str):
        print("create_tag command called with tags:", tags)
        
        custom_contents = self.bot.get_cog('CustomContents')
        tag_list = tags.split()
        created_tags = {}

        for tag in tag_list:
            print("Processing tag:", tag)
            db = SessionLocal()
            try:
                new_channel = await create_tag_and_channel(interaction.guild, tag, db)
                if new_channel:
                    print("Created new channel:", new_channel.name)
                    created_tags[tag] = new_channel.id
                else:
                    print("Tag already exists or failed to create channel for tag:", tag)
            except Exception as e:
                print("Error creating tag and channel for tag:", tag, e)
            finally:
                db.close()

        # 全てのタグが既に存在する場合
        if not created_tags:
            print("All tags already exist.")
            if custom_contents:
                await custom_contents.send_embed_info(interaction, 'タグリスト', 'すべてのタグが既に存在します。')
            return

        # 作成したチャンネルのメッセージを作成
        if custom_contents:
            created_channels = ' '.join([f"<#{channel_id}>" for channel_id in created_tags.values()])
            print("Created channels:", created_channels)
            await custom_contents.send_embed_info(interaction, 'タグリスト', f'{created_channels} を作成しました。')

async def setup(bot):
    await bot.add_cog(CreateTags(bot))
