from sqlalchemy.orm import Session
import discord
import discord.utils
from datetime import datetime

from discord_memo.db.database import SessionLocal
from discord_memo.db.crud import get_tags_by_name, create_message_group
from discord.ext import commands
from typing import  List

from discord_memo import config


class MemoEmbed(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.color = config.MEMO_COLOR

    def create_embed(self, content:str, message_url:str, title:str=config.MEMO_TITLE)-> discord.Embed:
        embed = discord.Embed(title=title, color=self.color, description=content)
        # embed.set_footer(text="[https://ptb.discord.com/channels/762233175669473290/762233175669473293/1094025351593730149")
        # embed.add_field(
        # name="",
        # value="[元のメッセージ](https://ptb.discord.com/channels/762233175669473290/762233175669473293/1094025351593730149)",
        # inline=False)
        # embed.set_footer(icon_url="https://ptb.discord.com/channels/762233175669473290/762233175669473293/1094025351593730149")
        embed.url = message_url
        # embed.timestamp=
        return embed

    
    async def send_embed(self, interaction: discord.Interaction, channel_id_list:List[int], embed:discord.Embed) -> None:
         for channel_id in channel_id_list:
            channel = self.bot.get_channel(channel_id)
            try: 
                await channel.send(embed=embed)
            except:
                print(f"Channel with ID {channel_id} not found")
