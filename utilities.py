import os
from telethon.sync import TelegramClient
from dotenv import load_dotenv

# load .env file
load_dotenv()

# get bot token from .env file
BOT_TOKEN = os.getenv("BOT_TOKEN")

# get Telegram API from telegram.me from .env file
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")

# initialize bot session
client = TelegramClient("bot", API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# start bot session
client.start()