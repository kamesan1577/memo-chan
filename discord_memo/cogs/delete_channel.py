from sqlalchemy.orm import Session
import discord
from discord_memo.db.database import SessionLocal
from discord_memo.db.crud import get_channel_by_name


# 名前でチャンネルを指定､削除 なければNoneを返す
# DBの方の該当データのis_deletedをTrueにする
async def delete_channel(guild: discord.Guild, channel_name: str, db: Session):
    try:
        channel = get_channel_by_name(db, channel_name)
        if not channel:
            return None
        channel = guild.get_channel(channel.channel_id)
        if channel:
            await channel.delete()
        channel.is_deleted = True
        db.commit()
        return channel
    except Exception as e:
        db.rollback()
        print(f"Error deleting channel: {e}")
        return None
