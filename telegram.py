import asyncio
import os

from telethon import TelegramClient, events
import re
from youtube import youtube_download
from dotenv import load_dotenv

load_dotenv()
# Replace these values with your own API ID, API HASH, and bot token

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("BOT_TOKEN")


# Function to send a private message using a bot
client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

@client.on(events.NewMessage())
async def main(event: events.newmessage.NewMessage.Event):

    def is_youtube_link(text):
        youtube_pattern = re.compile(r"(?:https?:\/\/)?(?:www\.)?(?:youtu\.be\/|youtube\.com\/watch\?v=)([\w-]+)")
        match = youtube_pattern.match(text)
        return bool(match)

    if event.is_private and event.text == '/start':
        if event.sender.last_name is not None:
            await event.respond(f'''Salam, **{event.sender.first_name}** **{event.sender.last_name}**!
Mən göndərəcəyin Youtube linkini sənə MP3 formatında qaytarmaq üçün assistantam.
Sadəcə istədiyin Youtube linkini göndər və arxana söykən. 😉

⭐️ Üstünlüklərim:
➖ Fayllar orijinal keyfiyyətdə göndərilir. AAC 128 Kbps.
➖ Yalnızca musiqi deyil, videoları da MP3 formatına gətirirəm.

❕Əgər musiqi daha əvvəl başqası tərəfindən yüklənibsə, anında göndərəcəyəm.

🗄 İndirilen müzikleri kanalımda (https://t.me/joinchat/AAAAAEpNIFaaE_CgT1vTYQ) depoluyorum.''')
        else:
            await event.respond(f'''Salam, **{event.sender.first_name}** !
Mən göndərəcəyin Youtube linkini sənə MP3 formatında qaytarmaq üçün assistantam.
Sadəcə istədiyin Youtube linkini göndər və arxana söykən. 😉

⭐️ Üstünlüklərim:
➖ Fayllar orijinal keyfiyyətdə göndərilir. AAC 128 Kbps.
➖ Yalnızca musiqi deyil, videoları da MP3 formatına gətirirəm.

❕Əgər musiqi daha əvvəl başqası tərəfindən yüklənibsə, anında göndərəcəyəm.

🗄 İndirilen müzikleri kanalımda (https://t.me/joinchat/AAAAAEpNIFaaE_CgT1vTYQ) depoluyorum.''')

    else:

        try:
            if is_youtube_link(event.raw_text):
                new_file, yt_title = await youtube_download(event)
                await client.send_file(event.chat_id, new_file, caption=yt_title)

                os.remove(new_file)
            else:
                await client.send_message(event.chat_id, "Zəhmət olmasa yalnız youtube linki göndərin")

        except Exception as e:
            await client.send_message(event.chat_id, "Xəta baş verdi. Zəhmət olmasa yaş məhdudiyyəti olmayan Youtube linki göndərin.")





with client:
    client.run_until_disconnected()