from sqlalchemy.orm import Session
import discord
import discord.utils
import re

from discord_memo.db.database import SessionLocal
from discord_memo.db.crud import get_tags_by_name, create_message_group
from discord.ext import commands
from typing import Literal, List
from sqlalchemy.orm import Session

from discord_memo.db.schemas import FileEntryData, MessageData
from discord_memo.db.crud import create_message_group, get_tags_by_name
from discord_memo.cogs.error_handler import ErrorHandler


class MessageTools(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.error_handler = ErrorHandler

    async def add_message(
        self,
        interaction: discord.Interaction,
        tags: str,
        message_data_list: List[MessageData],
    ):
        db = SessionLocal()
        try:
            # Create tag
            custom_contents = self.bot.get_cog("CreateTags")
            await custom_contents.create_tag_util(interaction, tags)
            # get channel id
            tag_list = tags.split()
            tag_id_list = []
            for tag in tag_list:
                tag_id = self.tag2channel_id(tag)
                if tag_id is not  -1:
                    tag_id_list.append(tag_id)

            # create message group
            create_message_group(db, message_data_list, tag_id_list)
        finally:
            db.close()

    def get_message_link(self, interaction: discord.Interaction) -> str:
        return f"https://discord.com/channels/{interaction.guild_id}/{interaction.channel_id}/{interaction.id}"

    def create_message_data(self, interaction: discord.Interaction, content:str, file_entries:List[FileEntryData]=[]) -> MessageData:
        message_data = MessageData(
            message_id=interaction.id,
            content=content,
            message_link=self.get_message_link(interaction),
            file_entries=file_entries,
            )
        return message_data

    def fomat_tag(self, tag:str) -> str:
        if re.match(r'^<#\d+>$', tag):
            tag = tag.replace("<#", "#").replace(">", "")
        return tag[1:]


    #@breif discordからの引き数としてのtagを必ずidに返してくれる関数
    #@ 存在しえないtag(型不正など)の場合は-1を返す
    def tag2channel_id(self, tag:str):
        db = SessionLocal()
        try:
            if re.match(r"<#\d+>", tag):
                tag = tag.replace("<#", "")
                tag_id = tag.replace(">", "")
                return int(tag_id)

            elif re.match(r"#.+", tag):
                return get_tags_by_name(db, tag[1:])[0].channel_id
            else:
                return -1
        except Exception as e:
            print(e)

        finally:
            db.close()
