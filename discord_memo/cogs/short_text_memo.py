import sys
sys.path.append('../') # dbディレクト読み込みのため入れてる

import discord
from discord import app_commands
from discord.ext import commands
from discord_memo.db.database import SessionLocal

from discord_memo.cogs.utils import create_tag_and_channel
from discord_memo.db.crud import get_tag, create_tag

class ShortMemo(commands.Cog):
    def __init__(self, bot):
        """ショートメモを作成"""    
        self.bot = bot

    @app_commands.command(name='memo', description='メモを作成します。')
    async def short_text_memo(self, interaction: discord.Interaction, memo: str, *, tags: str):
        custom_contents = self.bot.get_cog('CustomContents')
        tag_list = tags.split()
        channel_ids = [] # 保存先ID
        created_tags = [] # 作成したタグ
        # タグを探索、なかったら新規作成
        for tag in tag_list:
            db = SessionLocal()
            try:
                # タグが存在する場合
                if tag.startswith('<#') and tag.endswith('>'):
                    print("Processing created tag:", tag)
                    channel_id = int(tag.strip('<#>'))
                    channel_ids.append(channel_id)
                    tag = get_tag(db, channel_id)
                    # タグがDB側に存在しない場合登録
                    if not tag:
                        print("Tag not found in DB, creating tag for channel:", channel_id)
                        channel = self.bot.get_channel(channel_id)
                        create_tag(db, channel_id, channel.name)
                        print("Created tag for channel:", channel.name)
                # タグが存在しない場合
                else:
                    # 最初に#が存在する場合は付与
                    print("Processing new tag:", tag)
                    channel = await create_tag_and_channel(interaction.guild, tag, db)
                    channel_ids.append(channel.id)
                    created_tags.append(channel.id)
            except Exception as e:
                print("Error creating tag and channel for tag:", tag, e)
            finally:
                db.close()
        # 新規作成したタグがあった場合その情報を送信
        if created_tags:
            created_channels = ' '.join([f"<{channel_id}>" for channel_id in created_tags])
            if custom_contents:
                await custom_contents.send_embed_info(interaction, 'タグリスト', f'{created_channels} を作成しました。')
            
            
async def setup(bot):
    await bot.add_cog(ShortMemo(bot))

