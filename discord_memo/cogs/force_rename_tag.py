import sys
sys.path.append('../') # dbディレクト読み込みのため入れてる

import discord
from discord import app_commands
from discord.ext import commands

from discord_memo.db.database import SessionLocal
from discord_memo.db.crud import update_tag

class ForceRenameTags(commands.Cog):
    """タグのみを強制的に修正（開発用コマンド）"""
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='force_rename_tag', description='タグのみを強制的に修正します。')
    async def force_rename_tag(self, interaction: discord.Interaction, channel_id: str, tag_new: str):
        print("force_rename_tag command called with tags:", channel_id, tag_new)
        db = SessionLocal()
        try:
            update_tag(db, int(channel_id), tag_new)
            print("Tag updated successfully")
            await interaction.response.send_message("Tag updated successfully")
        except Exception as e:
            print("Error updating tag:", e)
            await interaction.response.send_message("Error updating tag")
        finally:
            db.close()

async def setup(bot):
    await bot.add_cog(ForceRenameTags(bot))