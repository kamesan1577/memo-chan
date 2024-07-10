from sqlalchemy.orm import Session
import discord
from discord_memo.db.database import SessionLocal
from discord_memo.db.crud import create_tag, get_tags_by_name

async def create_tag_and_channel(guild: discord.Guild, tag_name: str, db: Session):
    """新規でタグとチャンネルを作成
    Args:
        guild: discord.Guild: サーバー
        tag_name: str: タグ名
        db: Session: DBセッション
    Returns:
        discord.TextChannel: 作成したチャンネル
    """
    try:
        # 新しいチャンネルを作成
        new_channel = await guild.create_text_channel(tag_name)
        create_tag(db, new_channel.id, tag_name)
        db.commit()
        return new_channel
    except Exception as e:
        db.rollback()
        print(f"Error creating tag and channel: {e}")
        return None
