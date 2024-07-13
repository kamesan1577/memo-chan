import discord
from discord import app_commands
from discord.ext import commands

from discord_memo.utils.sync_memo_channels import sync_memo_channels
from discord_memo.cogs.error_handler import ErrorHandler

class Setup(commands.Cog):
    """メモ用のカテゴリをなかったら作成
    """
    def __init__(self, bot):
        self.bot = bot
        self.error_handl = ErrorHandler(bot)

    @app_commands.command(name="setup", description="メモ用のカテゴリを作成します。")
    async def setup(self, interaction: discord.Interaction):
        print("setup command called")
        custom_contents = self.bot.get_cog("CustomContents")
        try:
            await sync_memo_channels(interaction.guild)
            await custom_contents.send_embed_info(interaction, "セットアップ", "メモ用のカテゴリを作成しました。")
            return
        except Exception as e:
            print("Error setting up memo channels:", e)
            raise e
        
    @setup.error
    async def raise_error_handler(
        self, interaction: discord.Interaction, error: app_commands.AppCommandError
    ):
        await self.error_handl.send_error(interaction, error)

async def setup(bot):
    await bot.add_cog(Setup(bot))