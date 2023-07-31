from pytube import YouTube
import os

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

    # result of success
    print(yt.title + " has been successfully downloaded.")

    return new_file, yt.title

