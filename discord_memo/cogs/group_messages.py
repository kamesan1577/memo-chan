import discord
from discord.ext import commands
from discord import app_commands
from discord_memo.db.database import SessionLocal
from discord_memo.db import crud
from discord_memo.cogs.utils import create_tag_and_channel


class GroupMessages(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.memo_active = {}
        self.memo_group = {}

    @app_commands.command(name="memo_start")
    async def memo_start(self, interaction: discord.Interaction):
        custom_contents = self.bot.get_cog("CustomContents")
        print("memo_start called by user:", interaction.user.id)
        # print("memo_active:", self.memo_active)
        if custom_contents:
            if (
                interaction.user.id not in self.memo_active
            ):  # 同一人物が複数サーバーでコマンドを実行した時にバグるのかわからない
                self.memo_active[interaction.user.id] = True
                self.memo_group[interaction.user.id] = []
                print("memo_active:", interaction.user.id)
                await custom_contents.send_embed_info(
                    interaction, "Info", "メモの記録を開始しました。"
                )
            else:
                print("this user is already in memo_active")
                await custom_contents.send_embed_error(
                    interaction, "Error", "既にメモの記録が開始されています。"
                )

    @app_commands.command(name="memo_end")
    async def memo_end(
        self,
        interaction: discord.Interaction,
        *,
        tags: str = None,  # タグなしメモは許容するんだっけ？
    ):
        custom_contents = self.bot.get_cog("CustomContents")
        print("memo_end called by user:", interaction.user.id)
        if custom_contents:
            if interaction.user.id in self.memo_active:
                self.memo_active.pop(interaction.user.id)
                await self.add_group_message(
                    interaction, tags, self.memo_group[interaction.user.id]
                )
                print("memo_deactive:", interaction.user.id)
                await custom_contents.send_embed_info(
                    interaction, "Info", "メモの記録を終了しました。"
                )
            else:
                print("this user is not in memo_active")
                await custom_contents.send_embed_error(
                    interaction, "Error", "メモの記録が開始されていません。"
                )

    async def record_message(self, message: discord.Message):
        # メッセージテーブルに登録
        db = SessionLocal()
        file_entries = []
        content = message.content
        message_link = message.jump_url
        if message.attachments:
            for attachment in message.attachments:
                file_entry = {
                    "is_binary_data": True,
                    "image_link": attachment.url,
                }
                file_entries.append(file_entry)

        saved_message = crud.create_message(
            db,
            content=content,
            message_link=message_link,
            file_entries=file_entries,
        )

        if not self.memo_group[message.author.id]:
            return
        self.memo_group[message.author.id].append(saved_message.id)

        db.close()

    async def add_group_message(
        self, interaction: discord.Interaction, tags: str, messages: list
    ):
        custom_contents = self.bot.get_cog("CustomContents")
        if custom_contents:
            db = SessionLocal()
            try:
                print("create_tag command called with tags:", tags)
                tag_list = tags.split()
                created_tags, new_tags = await create_tag_and_channel(
                    interaction.guild, tag_list
                )
                # TODO 新規タグを作成した旨を通知する

                for tag in created_tags.values():
                    for message in messages:
                        crud.create_tag2message(
                            db,
                            tag_id=tag.id,
                            message_id=message.id,
                            channel_id=tag.channel_id,
                        )
                        print(
                            "tag2message created:", tag.id, message.id, tag.channel_id
                        )
                for tag in new_tags.values():
                    for message in messages:
                        crud.create_tag2message(
                            db,
                            tag_id=tag.id,
                            message_id=message.id,
                            channel_id=tag.channel_id,
                        )
                        print(
                            "tag2message created:", tag.id, message.id, tag.channel_id
                        )
            except Exception as e:
                print("Error creating tag2message:", e)
                await interaction.response.send_message("Error creating tag2message")
            finally:
                db.close()

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        if message.author.id in self.memo_active:
            await self.record_message(message)


async def setup(bot):
    await bot.add_cog(GroupMessages(bot))
