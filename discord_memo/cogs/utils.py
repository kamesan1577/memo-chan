import re

from sqlalchemy.orm import Session
import discord
import discord.utils

from discord_memo.db.database import SessionLocal
from discord_memo.db.crud import create_tag, get_tags_by_name, get_tag
from typing import Literal


async def create_tag_and_channel(guild: discord.Guild, tag_name: list):
    """新規でタグとチャンネルを作成
    タグが存在するか確認し、存在しなかったら新規作成。
    以下特殊ケース
    Discord側を基準とするため以下条件の場合DBに登録
    1. タグがDiscordに存在する
    2. タグがDBに存在しない
    Args:
        guild: discord.Guild: サーバー
        tag_name: list: タグ名(<#\d+> #tag tag どの表記でも対応)
    Returns:
        created_tags: dict: {"channel_name" : discord.TextChannel, ...} : 作成したチャンネル
        new_tags: dict: {"channel_name" : discord.TextChannel, ...} : 新規作成したタグ
    """
    created_tags = {}
    new_tags = {}
    for tag in tag_name:
        db = SessionLocal()
        try:
            tag_type = get_tag_type(tag)
            print("Processing tag:", tag)
            # 既存タグの場合
            # <#\d+>が来た場合
            if tag_type == "existing_tag":
                print("Processing created tag in Discord:", tag)
                channel_id = int(tag.strip("<#>"))
                # タグがDBに存在しない場合登録
                print(get_tag(db, channel_id))
                if not get_tag(db, channel_id):
                    print("Tag not found in DB, creating tag for channel:", channel_id)
                    channel_name = guild.get_channel(channel_id).name
                    create_tag(db, channel_id, channel_name)
                    print("Created tag for channel:", channel_name)
                created_tags[tag] = guild.get_channel(channel_id)
            elif get_tags_by_name(db, tag):
                print("Processing created tag in DB:", tag)
                tag_db = get_tags_by_name(db, tag)[0]
                created_tags[tag_db.name] = guild.get_channel(tag_db.channel_id)
            # タグ新規作成
            # #が最初に来る場合
            elif tag_type == "new_tag":
                print("Processing new tag:", tag)
                # 新しいチャンネルを作成
                # #を削除
                tag = tag.lstrip("#")
                new_channel = await guild.create_text_channel(tag)
                # DBに登録
                create_tag(db, new_channel.id, tag)
                new_tags[tag] = new_channel
                print("Created new channel:", new_channel.name)
            # 文字列だけの場合
            else:
                print("Processing new tag:", tag)
                new_channel = await guild.create_text_channel(tag)
                create_tag(db, new_channel.id, tag)
                new_tags[tag] = new_channel
                print("Created new channel:", new_channel.name)
        except Exception as e:
            print("Error creating tag and channel for tag:", tag, e)
        finally:
            db.close()
    print(f"created tags:{created_tags}")
    print(f"new tags:{new_tags}")
    return created_tags, new_tags


def get_tag_type(text: str) -> Literal["new_tag", "existing_tag", "invalid_tag"]:
    if re.match(r"<#\d+>", text):
        return "existing_tag"
    elif re.match(r"#\d+", text):
        return "new_tag"
    else:
        return "invalid_tag"
