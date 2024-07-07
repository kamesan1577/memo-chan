import discord
from discord import app_commands
from discord.ext import commands


class Hello(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Hello cog is ready")

    @app_commands.command(name="hello", description="Hello!")
    async def hello(self, interaction: discord.Interaction):
        await interaction.response.send_message("Hello!")


async def setup(bot: commands.Bot):
    await bot.add_cog(Hello(bot))
