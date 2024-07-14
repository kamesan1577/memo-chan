import discord
from discord_memo import config

category_name = config.CATEGORY_NAME

async def fetch_memo_category(interaction: discord.Interaction) -> discord.CategoryChannel | None:
    """サーバー二存在するメモ用カテゴリのIDを取得
    もしカテゴリが存在しない場合は自動で作成する

    Args:
        interaction (discord.Interaction):
    Returns:
        category_id (int): 取得、作成したカテゴリのID
    """
    print("fetch_memo_category called")
    guild = interaction.guild
    try:
        if not guild:
            # エラーメッセージを送信
            print("No guild found")
        memo_category = discord.utils.get(guild.categories, name=category_name)
        # カテゴリがあるなしの処理
        if memo_category:
            return memo_category
        else:
            new_category = await guild.create_category(category_name, reason="メモ用カテゴリを作成しました。")
            return new_category
    except:
        print("Error getting memo category")
        return None