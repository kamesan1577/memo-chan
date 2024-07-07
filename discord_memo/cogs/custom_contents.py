import discord
from discord.ext import commands
from discord.ui import Button, View

class CustomContents(commands.Cog):
    """
    Embedを送信するためのcog
    """
    SUCSSER_COLOR = discord.Color.green()
    ERROR_COLOR = discord.Color.red()
    INFO_COLOR = discord.Color.blue()

    @staticmethod
    async def send_embed(interaction, title, description, color, buttons=None):
        """
        送信のための基本的な関数
        buttons = [
        {'label': '了解', 'style': discord.ButtonStyle.green, 'custom_id': 'acknowledge', 'callback': MessageManager.confirm_callback},
        {'label': 'キャンセル', 'style': discord.ButtonStyle.red, 'custom_id': 'cancel', 'callback': MessageManager.cancel_callback}
        ]
        """
        embed = discord.Embed(title=title, color=color, description=description)
        if buttons:
            view = View()
            for button_cofig in buttons:
                button = Button(
                    label=button_cofig['label'],
                    style=button_cofig['style'],
                    custom_id=button_cofig['custom_id']
                )
                button.callback = button_cofig['callback']
                view.add_item(button)
            await interaction.response.send_message(embed=embed, view=view)
        else:
            await interaction.response.send_message(embed=embed)

    @classmethod
    async def send_embed_success(cls, interaction, title, description):
        """
        成功embed
        """
        await cls.send_embed(interaction, title, description, cls.SUCSSER_COLOR, buttons=None)

    @classmethod
    async def send_embed_error(cls, interaction, title, description):
        """
        エラーembed
        """
        await cls.send_embed(interaction, title, description, cls.ERROR_COLOR, buttons=None)

    @classmethod
    async def send_embed_info(cls, interaction, title, description):
        """
        情報embed
        """
        await cls.send_embed(interaction, title, description, cls.INFO_COLOR, buttons=None)

async def setup(bot):
    await bot.add_cog(CustomContents(bot))