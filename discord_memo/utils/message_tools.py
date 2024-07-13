from sqlalchemy.orm import Session
import discord
import discord.utils

from discord_memo.db.database import SessionLocal
from discord_memo.db.crud import get_tags_by_name, create_message_group
from discord.ext import commands
from typing import Literal, List

from discord_memo.db.schemas import FileEntryData, MessageData
from discord_memo.db.crud import create_message_group, get_tags_by_name


class MessageTools(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

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
                tag_id = get_tags_by_name(db, tag[1:])[0].channel_id
                tag_id_list.append(tag_id)

            # create message group
            create_message_group(db, message_data_list, tag_id_list)
        finally:
            db.close()
