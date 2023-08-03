import os

from telethon import TelegramClient
from dotenv import load_dotenv

load_dotenv()

api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
channel_id = int(os.getenv("CHANNEL_ID"))

client = TelegramClient('client', api_id, api_hash).start()

async def search_messages(yt_title):
    messages = await client.get_messages(channel_id, search=yt_title, limit=1)
    return messages

