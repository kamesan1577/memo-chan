from dotenv import load_dotenv
import os

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

DISCORD_TOKEN = os.environ.get('DISCORD_TOKEN')
