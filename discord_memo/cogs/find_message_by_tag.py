from discord.ext import commands
from sqlalchemy.orm import Session

from discord_memo.db.crud import get_tags_by_name, get_tag2messages, get_message
from discord_memo.db.database import SessionLocal


class FindMessageByTag(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="find_message_by_tag")
    async def find_message_by_tag(self, ctx, *, tag_name: str):
        db: Session = SessionLocal()
        try:
            tags = get_tags_by_name(db, name=tag_name)
            if not tags:
                await ctx.send(f"タグ '{tag_name}' が見つかりませんでした。")
                return

            tag = tags[0]  # 最初のタグを使用
            tag2messages = get_tag2messages(db, tag_id=tag.id)
            if not tag2messages:
                await ctx.send(
                    f"タグ '{tag_name}' に関連するメッセージが見つかりませんでした。"
                )
                return

            messages = []
            for tag2message in tag2messages:
                message = get_message(db, message_id=tag2message.message_id)
                if message:
                    messages.append(message)

            if not messages:
                await ctx.send(
                    f"タグ '{tag_name}' に関連するメッセージが見つかりませんでした。"
                )
                return

            for message in messages:
                await ctx.send(
                    f"メッセージ: {message.content}\nリンク: {message.message_link}"
                )

        finally:
            db.close()


def setup(bot):
    bot.add_cog(FindMessageByTag(bot))
