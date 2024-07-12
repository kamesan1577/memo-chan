import discord
from discord import app_commands
from discord.ext import commands


class DeleteMessage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="delete_memo")
    async def delete_message(self, interaction: discord.Interaction):
        custom_contents = self.bot.get_cog("CustomContents")
        if custom_contents:
            await custom_contents.send_embed_success(
                interaction, "Success", "This is a Success message."
            )


async def setup(bot):
    await bot.add_cog(DeleteMessage(bot))
