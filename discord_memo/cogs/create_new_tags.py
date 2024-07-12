import discord
from discord import app_commands
from discord.ext import commands
from discord_memo.db.database import SessionLocal

from .utils import create_tag_and_channel


class CreateTags(commands.Cog):
    """タグを新規作成"""

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="create_tag", description="タグを新規作成します。")
    async def create_tag(self, interaction: discord.Interaction, *, tags: str):
        print("create_tag command called with tags:", tags)
        custom_contents = self.bot.get_cog("CustomContents")
        tag_list = tags.split()
        created_tags, new_tags = await create_tag_and_channel(
            interaction.guild, tag_list
        )
        if new_tags:
            new_tag = " ".join([f"<#{channel.id}>" for channel in new_tags.values()])
            if custom_contents:
                await custom_contents.send_embed_info(
                    interaction, "タグリスト", f"{new_tag} を作成しました。"
                )
        else:
            if custom_contents:
                await custom_contents.send_embed_info(
                    interaction, "タグリスト", "存在するタグ、もしくは無効な書式です。(/create_tag #tag)"
                )


async def setup(bot):
    await bot.add_cog(CreateTags(bot))
