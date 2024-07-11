import discord
from discord.ext import commands
from discord import app_commands
from discord_memo.db.database import SessionLocal
from discord_memo.db import crud


class GroupMessages(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.memo_active = {}

    @app_commands.command(name="memo_start")
    async def memo_start(self, interaction: discord.Interaction):
        self.memo_active[interaction.user.id] = True
        custom_contents = self.bot.get_cog("CustomContents")
        if custom_contents:
            if (
                interaction.user.id not in self.memo_active
            ):  # 同一人物が複数サーバーでコマンドを実行した時にバグるのかわからない
                self.memo_active[interaction.user.id] = True
                await custom_contents.send_embed_info(
                    interaction, "Info", "メモの記録を開始しました。"
                )
            else:
                await custom_contents.send_embed_error(
                    interaction, "Error", "既にメモの記録が開始されています。"
                )

    @app_commands.command(name="memo_end")
    async def memo_end(self, interaction: discord.Interaction):
        custom_contents = self.bot.get_cog("CustomContents")
        if custom_contents:
            if interaction.user.id in self.memo_active:
                self.memo_active.pop(interaction.user.id)
                await custom_contents.send_embed_info(
                    interaction, "Info", "メモの記録を終了しました。"
                )
            else:
                await custom_contents.send_embed_error(
                    interaction, "Error", "メモの記録が開始されていません。"
                )

    async def record_message(self, message: discord.Message):
        # メッセージテーブルに登録
        db = SessionLocal()
        is_binary_data = False
        image_link = ""
        content = message.content
        message_link = message.jump_url
        # FIXME 添付ファイルの最初の一個しか保存できない
        if message.attachments:
            is_binary_data = True
            image_link = message.attachments[0].url

        saved_message = crud.create_message(
            db,
            is_binary_data=is_binary_data,
            image_link=image_link,
            content=content,
            message_link=message_link,
        )
        # メッセージグループに登録
        message_group = crud.create_message_group(
            db, message.channel.id
        )  # このメソッドの使い方がわからん
        db.close()

    async def add_group_message(self):
        db = SessionLocal()
        tag_id_list = crud.get_tags_by_name(db, "hoge")  # TODO タグ判定関数を入れる
        tag_id = tag_id_list[0].channel_id
        # グループidをtag2messageに登録
        crud.create_tag2message(db, tag_id=tag_id, message_id=1)
        db.close()
        custom_contents = self.bot.get_cog("CustomContents")
        if custom_contents:
            messages = []
            for message in messages:
                # メッセージを送信
                continue

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        if message.author.id in self.memo_active:
            await self.record_message(message)


async def setup(bot):
    await bot.add_cog(GroupMessages(bot))
