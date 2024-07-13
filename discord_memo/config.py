from dotenv import load_dotenv
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

load_dotenv(os.path.join(parent_dir, ".env"))

DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")
SQLALCHEMY_DATABASE_URL = os.environ.get("SQLALCHEMY_DATABASE_URL")
CATEGORY_NAME = "memo-bot"
