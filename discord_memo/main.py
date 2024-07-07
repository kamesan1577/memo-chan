import asyncio
import discord
from discord.ext import commands
import config

intents = discord.Intents.default()


async def main():
    INITIAL_EXTENSIONS = [
        "cogs.hello",
    ]
    TOKEN = config.DISCORD_TOKEN

    bot = commands.Bot(command_prefix="/", intents=intents)

    async def load_extensions(bot):
        for extension in INITIAL_EXTENSIONS:
            await bot.load_extension(extension)

    @bot.event
    async def setup_hook() -> None:
        await bot.tree.sync()

    await load_extensions(bot)
    await bot.start(TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
