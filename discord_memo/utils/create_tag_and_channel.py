import sys
sys.path.append('../')

import discord

from discord_memo.utils.get_tag_type import get_tag_type
from discord_memo.utils.validator import is_valid_tag_name
from discord_memo.db.crud import get_tag, create_tag, get_tags_by_name
from discord_memo.db.database import SessionLocal


async def create_tag_and_channel(guild: discord.Guild, category_id: int, tag_name: list):
    """新規でタグとチャンネルを作成
    タグが存在するか確認し、存在しなかったら新規作成。
    以下特殊ケース
    Discord側を基準とするため以下条件の場合DBに登録
    1. タグがDiscordに存在する
    2. タグがDBに存在しない
    Args:
        guild: discord.Guild: サーバー
        category_id int: カテゴリID
        tag_name: list: タグ名(<#\d+> #tag tag どの表記でも対応)
    Returns:
        created_tags: dict: {"channel_name" : discord.TextChannel, ...} : 作成済みチャンネル
        new_tags: dict: {"channel_name" : discord.TextChannel, ...} : 新規作成したタグ
    """
    print(f"create_tag_and_channel called with tags: {tag_name}")
    created_tags = {}
    new_tags = {}
    
    for tag in tag_name:
        print(f"Processing tag: {tag}")
        tag_type = get_tag_type(tag)
        db = SessionLocal()
        
        try:
            if tag_type == "existing_tag":
                created_tags = await handle_existing_tag(db, guild, tag, created_tags)
            elif tag_type == "new_tag":
                created_tags, new_tags = await handle_new_tag(db, guild, tag, category_id, created_tags, new_tags)
            else:
                print(f"Invalid tag format: {tag}")
        except Exception as e:
            print(f"Error processing tag {tag}: {e}")
        finally:
            db.close()
    
    print(f"created_tags: {created_tags}")
    print(f"new_tags: {new_tags}")
    return created_tags, new_tags


async def handle_existing_tag(db, guild, tag, created_tags):
    """既存のタグを処理する関数"""
    channel_id = int(tag.strip("<#>"))
    try:
        if get_tag(db, channel_id):
            print(f"Channel found in Discord, tag found in DB: {tag}")
            created_tags[guild.get_channel(channel_id).name] = guild.get_channel(channel_id)
        else:
            print(f"Channel found in Discord, tag not found in DB: {tag}")
            new_tag_in_db = create_tag(db, channel_id, guild.get_channel(channel_id).name)
            created_tags[guild.get_channel(channel_id).name] = guild.get_channel(channel_id)
    except Exception as e:
        print(f"Error handling existing tag {tag}: {e}")
    return created_tags


async def handle_new_tag(db, guild, tag, category_id, created_tags, new_tags):
    """新規タグを作成する関数"""
    channel_name = tag[1:]
    if not is_valid_tag_name(channel_name):
        print(f"Validation Error: {tag}")
        return created_tags, new_tags
    
    try:
        existing_channel = discord.utils.get(guild.text_channels, name=channel_name)
        if existing_channel:
            if get_tags_by_name(db, channel_name):
                print(f"Channel found in Discord, tag found in DB: {tag}")
                created_tags[channel_name] = existing_channel
            else:
                print(f"Channel found in Discord, tag not found in DB: {tag}")
                new_tag_in_db = create_tag(db, existing_channel.id, channel_name)
                created_tags[channel_name] = existing_channel
        else:
            print(f"Channel not found in Discord, tag not found in DB: {tag}")
            new_channel = await guild.create_text_channel(channel_name, category=category_id)
            new_tag_in_db = create_tag(db, new_channel.id, channel_name)
            created_tags[channel_name] = new_channel
            new_tags[channel_name] = new_channel
    except Exception as e:
        print(f"Error handling new tag {tag}: {e}")
    return created_tags, new_tags