from typing import List

import discord
from discord import app_commands
from discord.ext import commands

# from discord_memo.cogs.error_handler import ErrorHandler

from discord_memo.db.schemas import MessageData, FileEntryData
from discord_memo.utils.message_tools import MessageTools


class Hello(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # self.error_handl = ErrorHandler(bot)
        self.add_message = MessageTools(bot)

    @commands.Cog.listener()
    async def on_ready(self):
        print("Hello cog is ready")

    @app_commands.command(name="hello", description="Hello!")
    async def hello(self, interaction: discord.Interaction):
        await interaction.response.send_message("Hello!")

    @app_commands.command(name="hello_db", description="Hello!")
    async def hello_db(self, interaction: discord.Interaction, tag:str):

        messages: List[MessageData] = [
            MessageData(
                message_id=1,
                content="message1",
                message_link="https://discord.com/channels/1/1",
                file_entries=[
                    FileEntryData(is_binary_data=False, image_link="https://example.com")
                ],
            ),
            MessageData(
                message_id=2,
                content="message2",
                message_link="https://discord.com/channels/1/2",
                file_entries=[
                    FileEntryData(is_binary_data=False, image_link="https://example.com")
                ],
            ),
            MessageData(
                message_id=3,
                content="message3",
                message_link="https://discord.com/channels/1/3",
                file_entries=[
                    FileEntryData(is_binary_data=False, image_link="https://example.com")
                ],
            ),
        ]

        # tag = "#test"
        await self.add_message.add_message(interaction, tag, messages)



    # @app_commands.command(name="hello_error", description="エラーデバッグ用")
    # async def hello_error(self, interaction: discord.Interaction):
    #     try:
    #         # raise ValueError("This is a forced error for testing purposes.")
    #         raise discord.errors.ConnectionClosed()
    #     except discord.DiscordException as e:
    #         print(f"エラーを送信: {e}")
    #     except ValueError as e:
    #         print(f"エラー発行")
    #         raise e

    # @hello_error.error
    # async def raise_error_handler(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
    #     await self.error_handl.send_error(interaction, error)

    

async def setup(bot: commands.Bot):
    await bot.add_cog(Hello(bot))
