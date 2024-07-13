import discord
from discord import app_commands
from discord.ext import commands
from discord_memo.cogs.error_handler import ErrorHandler


class CategoryManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.error_handl = ErrorHandler(bot)
        self.category_name = "memo-bot"

    @commands.has_permissions(manage_channels=True)
    async def fetch_memo_category(
        self, interaction: discord.Interaction
    ) -> discord.CategoryChannel | None:
        """サーバーに存在するメモ用カテゴリのIDを取得
        もしカテゴリが存在しない場合は自動で作成する

        Args:
            interaction (discord.Interaction):
            category_name (str):
        Returns:
            category_id (int): 取得、作成したカテゴリのID
        """
        guild = interaction.guild
        try:
            if not guild:
                # エラーメッセージを送信
                print("No guild found")
                return None
            memo_category = discord.utils.get(guild.categories, name=self.category_name)
            if memo_category:
                # カテゴリを返す
                return memo_category
            else:
                new_category = await guild.create_category(
                    self.category_name,
                    reason="メモ用カテゴリを作成しました。",
                )
                return new_category
        # except discord.Forbidden as e:
        #     print(f"Error creating memo category: {e}")
        #     return None
        # except discord.HTTPException as e:
        #     print(f"Error creating memo category: {e}")
        #     return None
        except Exception as e:
            print(f"Error getting memo category: {e}")
            return None

    @commands.has_permissions(manage_channels=True)
    async def sync_memo_channels(self, interaction: discord.Interaction):
        """メモ用カテゴリに存在するチャンネルを同期する

        Args:
            interaction (discord.Interaction):
        """
        guild = interaction.guild
        memo_category = await self.fetch_memo_category(interaction)
        if not memo_category:
            print("No memo category found")
            return

        for channel in memo_category.channels:
            print(channel.name)
            # TODO チャンネルとDBの内容を同期する関数


async def setup(bot):
    await bot.add_cog(CategoryManager(bot))
