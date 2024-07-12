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
        created_tags: dict: {"channel_name" : discord.TextChannel, ...} : 作成済みチャンネル
        new_tags: dict: {"channel_name" : discord.TextChannel, ...} : 新規作成したタグ
    """
    print("create_tag_and_channel called with tags:", tag_name)
    created_tags = {}
    new_tags = {}
    for tag in tag_name:
        print("Proccesing tag:", tag)
        db = SessionLocal()
        try:
            tag_type = get_tag_type(tag)
            # 形式が<#\d+>の場合
            if tag_type == "existing_tag":
                # タグがDBに存在しない場合
                if not get_tag(db, int(tag.strip("<#>"))):
                    print("Tag not found in DB, creating tag")
                    new_tag = create_tag(db, int(tag.strip("<#>")), tag)
                    print("New tag is:", new_tag)
                    new_tags[tag] = guild.get_channel(new_tag.channel_id)
                # タグがDBに存在する場合
                else:
                    print("Tag found in DB")
                    created_tags[tag] = guild.get_channel(int(tag.strip("<#>")))
            # 形式が#\.+の場合
            elif tag_type == "new_tag":
                # Discord側にすでにチャンネルが存在する場合DBだけに登録
                if discord.utils.get(guild.text_channels, name=tag.lstrip("#")):
                    print("Tag already exists in Discord")
                    print("Tag name is:", tag.lstrip("#"))
                    new_tag = create_tag(db, discord.utils.get(guild.text_channels, name=tag.lstrip("#")).id, tag)
                    print("New tag is:", new_tag)
                    new_tags[tag.lstrip("#")] = guild.get_channel(new_tag.channel_id)
                    continue
                tag_name = tag.lstrip("#")
                # Discordにチャンネル新規作成
                new_channel = await guild.create_text_channel(tag_name)
                # DBに新規作成
                new_tag = create_tag(db, new_channel.id, tag_name)
                print("New tag is:", new_tag)
                new_tags[tag.lstrip("#")] = new_channel
            # 形式が不正の場合
            elif tag_type == "invalid_tag":
                print("Invalid tag format")
                continue
        except Exception as e:
            print("Error creating tag and channel for tag:", tag, e)
        finally:
            db.close()
    print("Created tags:", created_tags)
    print("New tags:", new_tags)
    return created_tags, new_tags


def get_tag_type(text: str) -> Literal["new_tag", "existing_tag", "invalid_tag"]:
    if re.match(r"<#\d+>", text):
        return "existing_tag"
    elif re.match(r"#.+", text):
        return "new_tag"
    else:
        return "invalid_tag"
