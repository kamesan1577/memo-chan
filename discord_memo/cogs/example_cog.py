import discord
from discord import app_commands
from discord.ext import commands


class ExampleCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # cogがNone返す可能性あるのでif置いてます

    @app_commands.command(name="success")
    async def send_success(self, interaction: discord.Interaction):
        custom_contents = self.bot.get_cog("CustomContents")
        if custom_contents:
            await custom_contents.send_embed_success(
                interaction, "Success", "This is a Success message."
            )

    @app_commands.command(name="error")
    async def send_error(self, interaction: discord.Interaction):
        custom_contents = self.bot.get_cog("CustomContents")
        if custom_contents:
            await custom_contents.send_embed_error(
                interaction, "Error", "This is an Error message."
            )

    @app_commands.command(name="info")
    async def send_info(self, interaction: discord.Interaction):
        custom_contents = self.bot.get_cog("CustomContents")
        if custom_contents:
            await custom_contents.send_embed_info(
                interaction, "Info", "This is an Info message."
            )


async def setup(bot):
    await bot.add_cog(ExampleCog(bot))
