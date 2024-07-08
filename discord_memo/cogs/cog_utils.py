from sqlalchemy.orm import Session

import discord
from discord.ext import commands

from discord_memo.db.crud import create_tag

class CreateNewTagandChannel(commands.Cog):
    """タグとチャンネルを新規作成"""
    def __init__(self, bot):
        self.bot = bot

        async def create_tag_and_channel(self, db: Session, guild: discord.guild, tag_name: str):
            """新規でタグとチャンネルを作成
            Args:
                db: Session: DBセッション
                guild: discord.guild: サーバー
                tag_name: str: タグ名
            Returns:
                channel_id: int: 新規作成したチャンネルのID
            """
            new_channel = await guild.create_text_channel(tag_name)
            await create_tag(db, new_channel.id, tag_name)
            return new_channel.id
        
async def setup(bot):
    await bot.add_cog(CreateNewTagandChannel(bot))