import asyncio
import discord
import os
from discord.ext import commands
from discord_memo.db.database import Base, engine
from discord_memo import config

intents = discord.Intents.default()

async def main():
	extensions = []
	current_dir = os.path.dirname(os.path.abspath(__file__))
	for cog in os.listdir(os.path.join(current_dir, "cogs")):
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
	Base.metadata.create_all(bind=engine)
	asyncio.run(main())
