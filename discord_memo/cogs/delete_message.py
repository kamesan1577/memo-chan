import discord
from discord import app_commands
from discord.ext import commands


# ユーザーがメッセージをDiscord上で削除したのを検知し、DBからも削除する
class DeleteMessage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        print("削除されたメッセージのID:"+str(message.id))
        # このメッセージIDでMessageテーブルを探索､group_idを取得
        # 

async def setup(bot):
    await bot.add_cog(DeleteMessage(bot))
