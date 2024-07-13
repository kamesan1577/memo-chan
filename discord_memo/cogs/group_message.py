import discord
from dataclasses import dataclass
from discord.ext import commands
from discord import app_commands
from discord_memo.db.schemas import MessageData, FileEntryData
from discord_memo.utils.create_tag_and_channel import create_tag_and_channel
from discord_memo.utils.message_tools import MessageTools


class GroupMessages(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.message_tools = MessageTools(bot)
        self.memo_active = {}
        self.memo_group = {}

    @app_commands.command(name="memo_start", description="メモの記録を開始します。")
    async def memo_start(self, interaction: discord.Interaction):
        custom_contents = self.bot.get_cog("CustomContents")
        print("memo_start called by user:", interaction.user.id)
        key = (interaction.user.id, interaction.guild.id)
        # print("memo_active:", self.memo_active)
        if custom_contents:
            if key not in self.memo_active:
                self.memo_active[key] = True
                self.memo_group[key] = []
                print("memo_active:", key)
                await custom_contents.send_embed_info(
                    interaction, "Info", "メモの記録を開始しました。"
                )
            else:
                print("this user is already in memo_active")
                await custom_contents.send_embed_error(
                    interaction, "Error", "既にメモの記録が開始されています。"
                )

    @app_commands.command(name="memo_end", description="メモの記録を終了します。")
    async def memo_end(
        self,
        interaction: discord.Interaction,
        tags: str,  # タグなしメモは許容するんだっけ？
    ):
        custom_contents = self.bot.get_cog("CustomContents")
        print("memo_end called by user:", interaction.user.id)
        key = (interaction.user.id, interaction.guild.id)
        if custom_contents:
            if key in self.memo_active:
                print("memo_group:", self.memo_group[key])
                self.memo_active.pop(key)
                await self.message_tools.add_message(
                    interaction, tags, self.memo_group[key]
                )
                print("memo_deactive:", key)
                await custom_contents.send_embed_info(
                    interaction, "Info", "メモの記録を終了しました。"
                )
            else:
                print("this user is not in memo_active")
                await custom_contents.send_embed_error(
                    interaction, "Error", "メモの記録が開始されていません。"
                )

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        key = (message.author.id, message.guild.id)
        if key in self.memo_active:
            await self.record_message(message)

    async def record_message(self, message: discord.Message):
        # メッセージテーブルに登録
        file_entries = None
        if message.attachments:
            file_entries = []
            for attachment in message.attachments:
                print(attachment.url)
                file_entries.append(
                    FileEntryData(is_binary_data=False, image_link=attachment.url)
                )
        message_data = MessageData(
            message_id=message.id,
            content=message.content,
            message_link=message.jump_url,
            file_entries=file_entries,
        )
        key = (message.author.id, message.guild.id)
        self.memo_group[key].append(message_data)
        print("message recorded")


async def setup(bot):
    await bot.add_cog(GroupMessages(bot))
