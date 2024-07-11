import re

from sqlalchemy.orm import Session
import discord
from discord_memo.db.database import SessionLocal
from discord_memo.db.crud import create_tag, get_tags_by_name, get_tag

async def create_tag_and_channel(guild: discord.Guild, tag_name: list):
    """新規でタグとチャンネルを作成
    タグが存在するか確認し、存在しなかったら新規作成。
    Discord側を基準とするため以下条件の場合DBに登録
    1. タグがDiscordに存在する
    2. タグがDBに存在しない
    Args:
        guild: discord.Guild: サーバー
        tag_name: list: タグ名(<#\d+> #tag tag どの表記でも対応)
    Returns:
        created_tags: dict: {"channel_name" : discord.TextChannel, ...}作成したチャンネル
        new_tags: dict: {"channel_name" : discord.TextChannel, ...} 新規作成したタグ
    """
    created_tags = {}
    new_tags = {}
    for tag in tag_name:
        db = SessionLocal()
        try:
            # <#\d+>が来た場合
            if re.match(r'<#\d+>', tag):
                print("Processing created tag in Discord:", tag)
                channel_id = int(tag.strip('<#>'))
                # タグがDBに存在しない場合登録
                if not get_tag(db, channel_id):
                    print("Tag not found in DB, creating tag for channel:", channel_id)
                    channel_name = guild.get_channel(channel_id).name
                    create_tag(db, channel_id, channel_name)
                    print("Created tag for channel:", channel_name)
                created_tags[tag] = guild.get_channel(channel_id)
            # タグ新規作成の場合
            # #が最初に来る場合
            if re.match(r'#', tag):
                print("Processing new tag:", tag)
                # 新しいチャンネルを作成
                # #を削除
                tag = tag.lstrip('#')
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
    return created_tags, new_tags