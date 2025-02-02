import sys

sys.path.append("../")

import discord
from discord import app_commands
from discord.ext import commands


from discord_memo.utils.create_tag_and_channel import create_tag_and_channel
from discord_memo.utils.fetch_memo_category import fetch_memo_category
from discord_memo.utils.sync_memo_channels import sync_memo_channels
from discord_memo import config


class CreateTags(commands.Cog):
    """タグを新規作成"""

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="create_tag", description="タグを新規作成します。")
    async def create_tag(self, interaction: discord.Interaction, tags: str):
        await self.create_tag_util(interaction, tags)

    async def create_tag_util(self, interaction: discord.Interaction, tags: str):
        print("create_tag command called with tags:", tags)
        custom_contents = self.bot.get_cog("CustomContents")
        # discordとDBとの同期関係
        await sync_memo_channels(interaction)
        category_id = await fetch_memo_category(interaction)

        tag_list = tags.split()
        created_tags, new_tags = await create_tag_and_channel(
            guild=interaction.guild, category_id=category_id, tag_name=tag_list
        )
        print(type(created_tags))
        print(type(new_tags))
        print(f"create_tags{created_tags}")
        print(f"new_tags{new_tags}")
        if new_tags:
            new_tag = " ".join([f"<#{channel.id}>" for channel in new_tags.values()])
            if custom_contents:
                await custom_contents.send_embed_info(
                    interaction, "タグリスト", f"{new_tag} を作成しました。"
                )
        elif created_tags == {}:
            if custom_contents:
                await custom_contents.send_embed_info(
                    interaction,
                    f"タグリスト",
                    "無効な書式です。\n ex)`/create_tag #tag`",
                )
        else:
            if custom_contents:
                await custom_contents.send_embed_info(
                    interaction, "タグリスト", "存在するタグです"
                )


async def setup(bot):
    await bot.add_cog(CreateTags(bot))
