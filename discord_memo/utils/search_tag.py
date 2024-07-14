import sys

sys.path.append("../")

import discord
from typing import List
from discord_memo.db.crud import get_message_groups_by_tag
from discord_memo.db.database import SessionLocal


async def search_memo(
    interaction: discord.Interaction,
    tag_id_list: List[int],
    sort_from_old: bool = False,
    skip: int = -0,
) -> List:
    """与えられたタグで登録されたメモ一覧を10個取得

    Args:
        interaction (discord.Interaction):
        tag_id_list (List[int]): 検索したいタグのIDのリスト

    Returns:
        message_group (List): 検索結果のメッセージグループのリスト
    """
    db = SessionLocal()
    message_group_list = []
    try:
        
        message_group_list = get_message_groups_by_tag(db, tag_id_list)
    except Exception as e:
        print(f"Error searching tag: {e}")
    finally:
        db.close()
    return message_group_list
