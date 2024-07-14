import discord
from discord import app_commands
from discord.ext import commands
from discord_memo.utils.search_tag import search_memo
from discord_memo.utils.get_tag_type import get_tag_type


class SendSearchResult(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # cogがNone返す可能性あるのでif置いてます

    @app_commands.command(
        name="search", description="指定されたタグのメモを検索します。"
    )
    async def search(
        self, interaction: discord.Interaction, tags: str, sort_from_old: bool = False
    ):
        custom_contents = self.bot.get_cog("CustomContents")
        await interaction.response.defer()
        if custom_contents:
            tag_list = tags.split()
            channel_id_list = []  # Corrected typo here
            for tag in tag_list:
                tag_type = get_tag_type(tag)
                if (
                    tag_type == "existing_tag"
                ):  # FIXME DBに存在しないチャンネルIDが入ってしまう
                    channel_id_list.append(int(tag.strip("<#>")))
                else:
                    await custom_contents.send_embed_error(
                        interaction, "エラー", tag + " は存在しないタグです。"
                    )
                    return
            search_result = await search_memo(
                interaction, channel_id_list, sort_from_old
            )  # TODO ボタンでページングできるようにする
            if search_result:
                for result in search_result:
                    print("search_result:", result.messages)
                    await custom_contents.send_embed_info(
                        interaction, "検索結果", result.messages, followup=True
                    )
            else:
                await custom_contents.send_embed_info(
                    interaction, "検索結果", "検索結果がありません。", followup=True
                )


async def setup(bot):
    await bot.add_cog(SendSearchResult(bot))
