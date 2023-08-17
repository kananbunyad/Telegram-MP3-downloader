from pytube import YouTube
import os
import music_tag

def get_yt_title(event):
    yt = YouTube(event.raw_text
                 )
    return yt.title


async def youtube_download(event):
    yt = YouTube(event.raw_text
                 )

    video = yt.streams.filter(only_audio=True).first()

    # download the file
    out_file = video.download(output_path=".")

    # save the file
    base, ext = os.path.splitext(out_file)
    new_file = base + '.mp3'
    os.rename(out_file, new_file)
    f = music_tag.load_file(f'{new_file}')
    f['title'] = yt.title
    f['artist'] = yt.author

    # result of success
    print(yt.title + " has been successfully downloaded.")

    return new_file, yt.title, yt.author, yt.length
