import sys
sys.path.append('../')  # dbディレクト読み込みのため入れてる

import discord
from discord import app_commands
from discord.ext import commands

from discord_memo.db.database import SessionLocal
from discord_memo.utils.get_tag_type import get_tag_type
from discord_memo.utils.create_tag_and_channel import create_tag_and_channel
from discord_memo.utils.validator import is_valid_tag_name
from discord_memo.db.crud import update_tag, get_tag
from discord_memo.utils.fetch_memo_category import fetch_memo_category
from discord_memo.utils.sync_memo_channels import sync_memo_channels


class RenameTags(commands.Cog):
    """タグを修正"""
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='rename_tag', description='タグを修正します。')
    async def rename_tag(self, interaction: discord.Interaction, tag_old: str, tag_new: str):
        print("rename_tag command called with tags:", tag_old, tag_new)
        custom_contents = self.bot.get_cog('CustomContents')
        tag_old_type = get_tag_type(tag_old)
        tag_new_type = get_tag_type(tag_new)

        try:
            tag_old_channel_id = int(tag_old.strip("<#>"))
            tag_old_channel = interaction.guild.get_channel(tag_old_channel_id)
            if tag_old_channel is None:
                if custom_contents:
                    await custom_contents.send_embed_error(interaction, 'エラー', '修正するタグのチャンネルが存在しません。')
                return
            # バリデータ
            if is_valid_tag_name(tag_new[1:]) is False:
                if custom_contents:
                    await custom_contents.send_embed_error(interaction, 'エラー', '修正するタグの形式が正しくありません。')
                return
            tag_old_channel_name = tag_old_channel.name
        except ValueError:
            if custom_contents:
                await custom_contents.send_embed_error(interaction, 'エラー', '修正するタグの形式が正しくありません。')
            return

        # 条件を「tag_oldが'existing_tag'かつtag_newが'new_tag'である場合」に修正
        if tag_old_type != "existing_tag" or tag_new_type != "new_tag":
            if custom_contents:
                await custom_contents.send_embed_error(interaction, 'エラー', 'タグの形式が正しくありません。')
            return

        # discordとDBとの同期関係
        await sync_memo_channels(interaction)
        category_id = await fetch_memo_category(interaction)

        tag_new = tag_new.lstrip("#")

        dict_discordTextChannel, new_tag = await create_tag_and_channel(guild=interaction.guild, 
                                                                   category_id=category_id,
                                                                   tag_name=[tag_old])
        #TODO 処理が複雑化してるので直せたら直す
        discordTextChannel = dict_discordTextChannel[next(iter(dict_discordTextChannel))]
        db = SessionLocal()
        try:
            print("Updating tag and channel for tag:", discordTextChannel.id)
            update_tag(db, discordTextChannel.id, tag_new)  
            new_channel = await discordTextChannel.edit(name=tag_new)
            if custom_contents:
                await custom_contents.send_embed_info(interaction, 'タグリスト', f'{tag_old_channel_name} を <#{new_channel.id}> に修正しました。')
        except Exception as e:
            print("Error updating tag and channel for tag:", tag_old, e)
            if custom_contents:
                await custom_contents.send_embed_error(interaction, 'エラー', 'タグとチャンネルの更新中にエラーが発生しました。')
        finally:
            db.close()

    @commands.Cog.listener()
    async def on_guild_channel_update(self, before: discord.abc.GuildChannel, after: discord.abc.GuildChannel):
        if before.name != after.name:
            print(f"Channel renamed from {before.name} to {after.name}")
            db = SessionLocal()
            try:
                update_tag(db, after.id, after.name)
                print(f"Updated tag for channel {after.id} in database.")
            except Exception as e:
                print(f"Error updating tag for channel {after.id}: {e}")
            finally:
                db.close()

async def setup(bot):
    await bot.add_cog(RenameTags(bot))
