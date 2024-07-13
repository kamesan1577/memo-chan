import re
import time

from sqlalchemy.orm import Session
import discord
import discord.utils

from discord_memo.db.database import SessionLocal
from discord_memo.db.crud import create_tag, get_tags_by_name, get_tag, create_message,  create_message_group, add_to_message_group, create_tag2message
from discord.ext import commands
from typing import Literal, List


async def create_tag_and_channel(guild: discord.Guild, tag_name: list):
    # 
    # @brief 新規でタグとチャンネルを作成
    # タグが存在するか確認し、存在しなかったら新規作成。
    # 以下特殊ケース
    # Discord側を基準とするため以下条件の場合DBに登録
    # 1. タグがDiscordに存在する
    # 2. タグがDBに存在しない
    # Args:
    #     guild: discord.Guild: サーバー
    #     tag_name: list: タグ名(<#\d+> #tag tag どの表記でも対応)
    # Returns:
    #     created_tags: dict: {"channel_name" : discord.TextChannel, ...} : 作成済みチャンネル
    #     new_tags: dict: {"channel_name" : discord.TextChannel, ...} : 新規作成したタグ
    # 
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

class MessageTools(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
    
    async def add_message(self, interaction: discord.Interaction, tags: str, message_id_list: List[int]):
        # Create tag 
        print("!!!!!!!!!!!!!!!!!!!!")
        custom_contents = self.bot.get_cog('CreateTags')
        await custom_contents.create_tag_util(interaction, "#test443W")
        print("====================")

        tag_list = tags.split()
        tag_list = ["test443W"]

        db = SessionLocal()
        channel_id_list = []

        print("====================")
        # tagをchannel_idに変換
        for tag in tag_list:
            print(f"tag{tag}")
            # time.sleep(5)
            buf_tag = get_tags_by_name(db, tag)[0].channel_id
            print(f"buf_tag:{buf_tag}")
            channel_id_list.append(buf_tag)
            print(f"channe_id:{channel_id_list}")
        print(f"channe_id:{channel_id_list}")

        # Messageをmessagegroup DBに追加
        group_id = 0 # init group_id
        if len(message_id_list) == 1:
            group_id = create_message_group(db, message_id_list[0]).group_id
        else:
            for i in range(len(channel_id_list)):
                if i == 0:
                    group_id = create_message_group(db, message_id_list[0])
                else:
                    add_to_message_group(db, message_id_list[i+1], group_id)

        print(f"group_id:{group_id}")
        print(f"m_list{message_id_list}")
        print(f"tag_list{tag_list}")
        # tag2messageにグループを登録
        for channel_id in channel_id_list:
            for message_id in message_id_list:
                for tag_name in tag_list:
                    # TODO:get_tags_by_nameの部分が同じ名前を見つけたらやばい
                    # tag_id = get_tags_by_name(db, tag_name)[0]
                    # print(f"tag_id:{tag_id}")
                    print("ここまで?")
                    test = create_tag2message(db,
                                       channel_id,
                                       message_id,
                                       channel_id,
                                       group_id)
                    print(test)
                    print("666666666666666")

        print("##########################")
