import discord
from discord import app_commands
from discord.ext import commands
from discord_memo.db.crud import delete_all_node_message


# ユーザーがメッセージをDiscord上で削除したのを検知し、DBからも削除する
class DeleteMessage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        print("削除されたメッセージのID:"+str(message.id))
        delete_all_node_message(message.id)


async def setup(bot):
    await bot.add_cog(DeleteMessage(bot))
