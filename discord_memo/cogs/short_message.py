from typing import List

import discord
from discord import app_commands
from discord.ext import commands

from discord_memo import config
from discord_memo.db.crud import get_tags_by_name,add_node_message
from discord_memo.utils.memo_embed import MemoEmbed


from discord_memo.db.database import SessionLocal
from discord_memo.db.schemas import MessageData, FileEntryData
from discord_memo.utils.message_tools import MessageTools


class ShortMessage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.message_tools = MessageTools(bot)
        self.memo_embed = MemoEmbed(bot)

    @app_commands.command(name="memo", description="短いメモの追加")
    async def memo(
        self,
        interaction: discord.Interaction,
        message: str,
        tags: str,
        title: str = config.MEMO_TITLE,
    ):
        db = SessionLocal()
        try:
            message_data_list = self.message_tools.create_message_data(
                interaction, message
            )
            group_id = await self.message_tools.add_message(interaction, tags, [message_data_list])

            embed = self.memo_embed.create_embed(
                message, self.message_tools.get_message_link(interaction), title
            )
            channel_id_list = []
            for tag in tags.split():
                if tag is not -1:
                    channel_id_list.append(self.message_tools.tag2channel_id(tag))

            sent_list = await self.memo_embed.send_embed(interaction, channel_id_list, embed)
            for sent in sent_list:
                add_node_message(
                    db, sent, group_id
                )
            # message_id = sent.id
            # group_id = res
            # add_node_message(
            #     db, message_id, group_id
            # ) 

        except Exception as e:
            error_handler = self.bot.get_cog("ErrorHandler")
            await error_handler.send_error(interaction, e)
        finally:
            db.close()


async def setup(bot: commands.Bot):
    await bot.add_cog(ShortMessage(bot))
