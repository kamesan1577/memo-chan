import discord
from discord import app_commands
from discord.ext import commands
from typing import overload


class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @app_commands.command(name="raise_error", description="エラーデバッグ用")
    async def raise_error(self, interaction: discord.Interaction):
        try:
            raise ValueError("This is a forced error for testing purposes.")
        except discord.DiscordException as e:
            print(f"エラーを送信: {e}")
        except ValueError as e:
            print(f"エラー発行")
            raise e

    @raise_error.error
    async def raise_error_handler(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        await self.send_error(interaction, error)


    async def send_error(self, interaction: discord.Interaction, error: Exception) -> None:
        custom_contents = self.bot.get_cog('CustomContents')
        error_details = f"🎉**{type(error).__name__}**🎉\n\n{error}👍👍👍 \n **See** 🥳: https://github.com/kamesan1577/geek-camp-vol8/issues"
        await custom_contents.send_embed_error(interaction, 'ERROR ( ☞◔ ౪◔)☞', error_details)


async def setup(bot):
    await bot.add_cog(ErrorHandler(bot))
