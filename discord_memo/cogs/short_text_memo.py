import sys
sys.path.append('../') # dbディレクト読み込みのため入れてる

import discord
from discord import app_commands
from discord.ext import commands
from discord_memo.db.database import SessionLocal

from discord_memo.cogs.utils import create_tag_and_channel
from discord_memo.db.crud import create_message


class ShortMemo(commands.Cog):
    def __init__(self, bot):
        """ショートメモを作成"""    
        self.bot = bot

    @app_commands.command(name='memo', description='メモを作成します。')
    async def short_text_memo(self, interaction: discord.Interaction, memo: str, *, tags: str):
        custom_contents = self.bot.get_cog('CustomContents')
        tag_list = tags.split()
        # タグ新規作成
        created_tags, new_tags = await create_tag_and_channel(interaction.guild, tag_list)
        if new_tags:
            new_tag = ' '.join([f"<#{channel.id}>" for channel in new_tags.values()])
            if custom_contents:
                await custom_contents.send_embed_info(interaction, 'タグリスト', f'{new_tag} を作成しました。')
        db = SessionLocal()
        try:
            # Messageテーブルに登録
            create_message(db, False, content=memo, message_link=interaction.message.link)
            
            
async def setup(bot):
    await bot.add_cog(ShortMemo(bot))

