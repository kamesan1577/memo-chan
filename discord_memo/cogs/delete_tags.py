import discord
from discord import app_commands
from discord.ext import commands
from discord_memo.cogs.utils import get_tag_type
from discord_memo.db import crud
from discord_memo.db.database import SessionLocal


class DeleteTags(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def delete_tag(self, tag_id: int):
        print(f"Attempting to delete tag with ID: {tag_id}")
        db = SessionLocal()
        try:
            tag = crud.get_tag(db, tag_id)
            if not tag:
                print(f"Tag not found or already deleted: {tag_id}")
                return None

            # タグの論理削除を実行
            deleted_tag = crud.delete_tag(db, tag_id)
            print(f"Tag deleted: {deleted_tag}")

            # チャンネルの削除を試みる
            try:
                channel = self.bot.get_channel(deleted_tag.channel_id)
                if channel:
                    await channel.delete(reason="Associated tag was deleted")
                    print(f"Channel deleted: {deleted_tag.channel_id}")
                else:
                    print(f"Channel not found: {deleted_tag.channel_id}")
            except Exception as e:
                print(f"Error deleting channel: {e}")
                # db.rollback()
                return None
            else:
                # db.commit()
                return deleted_tag
        except Exception as e:
            print(f"Error deleting tag: {e}")
            # db.rollback()
            return None
        finally:
            db.close()

    # コマンドによるチャンネル削除時
    @app_commands.command(name="delete_tag", description="タグを削除します。")
    async def delete_tag_command(self, interaction: discord.Interaction, tag_name: str):
        await interaction.response.defer()
        custom_contents = self.bot.get_cog("CustomContents")
        if custom_contents:
            print("delete_tag command called with tag_name:", tag_name)
            tag_type = get_tag_type(tag_name)
            if tag_type == "existing_tag":
                print("Processing tag:", tag_name)
                tag_id = int(tag_name.strip("<#>"))
                deleted_tag = await self.delete_tag(tag_id)  # FIXME ここで処理が止まる
                print("Deleted tag:", deleted_tag)
                if not deleted_tag:
                    await custom_contents.send_embed_error(
                        interaction, "Error", "削除に失敗しました", followup=True
                    )
                    return
                await custom_contents.send_embed_success(
                    interaction,
                    "Success",
                    f"{deleted_tag.name}が削除されました",
                    followup=True,
                )
            else:
                await custom_contents.send_embed_error(
                    interaction, "Error", "存在しないタグです", followup=True
                )
                return

    # ユーザーによるチャンネル削除検知時
    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        print("Channel deleted")
        channel_id = channel.id
        print(f"Channel ID: {channel_id}")
        deleted_tag = await self.delete_tag(channel_id)
        if not deleted_tag:
            return
        print(f"Deleted tag: {deleted_tag.name}")


async def setup(bot):
    await bot.add_cog(DeleteTags(bot))
