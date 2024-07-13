import discord

import discord_memo.utils.fetch_memo_category as fetch_memo_category
from discord_memo.utils.create_tag_and_channel import create_tag_and_channel

async def sync_memo_channels(interaction: discord.Interaction):
    """メモ用カテゴリに存在するチャンネルを同期する
    
    Args:
        interaction (discord.Interaction):
    Returns:
        category_id (int): 取得、作成したカテゴリのID
    """
    print("sync_memo_channels called")
    guild = interaction.guild
    memo_category = await fetch_memo_category(interaction)
    if not memo_category:
        print("No memo category found")
        return
    else:
        for channel in memo_category.channels:
            print(channel.name)
            created_tags, new_tags = await create_tag_and_channel(guild, memo_category.id, [channel.name])
            print(f"created_tags: {created_tags}")
        return
    
    