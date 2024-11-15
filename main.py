import os

from telethon import TelegramClient, events

from telethon.tl.types import DocumentAttributeAudio

from youtube import youtube_download, get_yt_title
from dotenv import load_dotenv
from regex import is_youtube_link
from group import search_messages

load_dotenv()

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("BOT_TOKEN")
channel_id = int(os.getenv("CHANNEL_ID"))

# Function to send a private message using a bot
client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

@client.on(events.NewMessage())
async def main(event: events.newmessage.NewMessage.Event):

    if event.is_private and event.text == '/start':
        if event.sender.last_name is not None:
            await event.respond(f'''Salam, **{event.sender.first_name}** **{event.sender.last_name}**!
Mən göndərəcəyin Youtube linkini sənə MP3 formatında qaytarmaq üçün assistantam.
Sadəcə istədiyin Youtube linkini göndər və arxana söykən. 😉

⭐️ Üstünlüklərim:
➖ Fayllar orijinal keyfiyyətdə göndərilir. AAC 128 Kbps.
➖ Yalnızca musiqi deyil, videoları da MP3 formatına gətirirəm.

❕Əgər musiqi daha əvvəl başqası tərəfindən yüklənibsə, anında göndərəcəyəm.

🗄 Yüklənən musiqiləri [kanalımda](https://t.me/musicalaze) depolayıram.''')
        else:
            await event.respond(f'''Salam, **{event.sender.first_name}** !
Mən göndərəcəyin Youtube linkini sənə MP3 formatında qaytarmaq üçün assistantam.
Sadəcə istədiyin Youtube linkini göndər və arxana söykən. 😉

⭐️ Üstünlüklərim:
➖ Fayllar orijinal keyfiyyətdə göndərilir. AAC 128 Kbps.
➖ Yalnızca musiqi deyil, videoları da MP3 formatına gətirirəm.

❕Əgər musiqi daha əvvəl başqası tərəfindən yüklənibsə, anında göndərəcəyəm.

🗄 Yüklənən musiqiləri [kanalımda](https://t.me/musicalaze) depolayıram.''')

    else:

        if is_youtube_link(event.raw_text):
            yt_title = get_yt_title(event)
            paired_message = await search_messages(yt_title)
            if paired_message:
                await client.forward_messages(event.chat_id, paired_message)
            else:
                new_file, yt_title, author_name, duration = await youtube_download(event)
                attributes = [DocumentAttributeAudio(duration=duration, title=yt_title, performer=author_name)]
                sent_message = await client.send_file(event.chat_id, new_file, attributes=attributes)
                await client.forward_messages(channel_id, sent_message, silent=True)

                os.remove(new_file)
        else:
            await client.send_message(event.chat_id, "Zəhmət olmasa yalnız youtube linki göndərin")


client.run_until_disconnected()
