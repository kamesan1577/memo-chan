import discord
from discord import app_commands
from discord.ext import commands

from discord_memo.cogs.error_handler import ErrorHandler


class Hello(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.error_handl = ErrorHandler(bot)

    @commands.Cog.listener()
    async def on_ready(self):
        print("Hello cog is ready")

    @app_commands.command(name="hello", description="Hello!")
    async def hello(self, interaction: discord.Interaction):
        await interaction.response.send_message("Hello!")


    @app_commands.command(name="hello_error", description="エラーデバッグ用")
    async def hello_error(self, interaction: discord.Interaction):
        try:
            # raise ValueError("This is a forced error for testing purposes.")
            raise discord.errors.ConnectionClosed()
        except discord.DiscordException as e:
            print(f"エラーを送信: {e}")
        except ValueError as e:
            print(f"エラー発行")
            raise e

    @hello_error.error
    async def raise_error_handler(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        await self.error_handl.send_error(interaction, error)

    

async def setup(bot: commands.Bot):
    await bot.add_cog(Hello(bot))
