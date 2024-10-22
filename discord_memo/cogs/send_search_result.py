import discord
from discord import app_commands
from discord.ext import commands
from discord_memo.db.database import SessionLocal

from discord_memo.utils.search_tag import search_memo
from discord_memo.utils.get_tag_type import get_tag_type
from discord_memo.utils.message_tools import MessageTools
from discord_memo.utils.memo_embed import MemoEmbed
from discord_memo.db.crud import get_message_groups_by_tag, _get_message_by_group_id, _get_file_entry_by_message_id
from sqlalchemy import Text


class SendSearchResult(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.message_tool = MessageTools(bot)
        self.memo_embed = MemoEmbed(bot)


    @app_commands.command(
        name="search", description="指定されたタグのメモを検索します。"
    )
    async def search(
        self, interaction: discord.Interaction, tags: str, sort_from_old: bool = False
    ):
        custom_contents = self.bot.get_cog("CustomContents")
        if custom_contents:
            tag_list = tags.split()
            channel_id_list = []  # Corrected typo here
            for tag in tag_list:
                channel_id = self.message_tool.tag2channel_id(tag)
                if channel_id != -1:
                    channel_id_list.append(channel_id)

            db = SessionLocal()
            try:
                await interaction.response.send_message("検索中...")
                message = await interaction.original_response()
                group_list = await search_memo(interaction, channel_id_list)
                if group_list == []:
                    await message.edit(content="**該当のメッセージは見つかりませんでした**")
                else:
                    message_result = await message.edit(content="検索結果を作成中...")
                    thread = await message.create_thread(name=f"検索結果",auto_archive_duration=60)
                    await thread.send("# 検索結果") 
                    for group in group_list:
                        message_list = _get_message_by_group_id(db, group.group_id)
                        content_buf = ""
                        binaly_link_list = []
                        for message in message_list:
                            file_entry = _get_file_entry_by_message_id(db, message.message_id)
                            if  file_entry != None:
                                for file in file_entry:
                                    binaly_link_list.append(file.image_link)
                            content_buf += message.content  # This is now a string

                        memo_embed = self.memo_embed.create_embed(content=content_buf, title="Memo",message_url=message_list[0].message_link)
                        if binaly_link_list == []: 
                            await thread.send(embed=memo_embed)
                        else:
                            await thread.send(embed=memo_embed)
                            for binaly_link in binaly_link_list:
                                await thread.send(binaly_link)
                        print(message_list)

                    await message_result.edit(content=f"## 検索tag\n {', '.join(tag_list)}")
            except Exception as e:
                print(e)


async def setup(bot):
    await bot.add_cog(SendSearchResult(bot))
