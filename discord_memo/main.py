import asyncio
import discord
import os
from discord.ext import commands
from discord_memo import config

intents = discord.Intents.default()


async def main():
	extensions = []
	for cog in os.listdir("discord_memo/cogs"):  # これってハードコードでいいんだろうか
		if cog.endswith(".py"):
			extensions.append(f"cogs.{cog[:-3]}")

	TOKEN = config.DISCORD_TOKEN

	bot = commands.Bot(command_prefix="/", intents=intents)

	async def load_extensions(bot):
		for extension in extensions:
			try:
				await bot.load_extension(extension)
				print(f"Loaded extesion: {extension}")
			except Exception as e:
				print(f"Failed to load extension {extension}: {e}")

	@bot.event
	async def setup_hook() -> None:
		await bot.tree.sync()

	await load_extensions(bot)
	await bot.start(TOKEN)


if __name__ == "__main__":
	asyncio.run(main())
