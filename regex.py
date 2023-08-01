import re


def is_youtube_link(text):
    youtube_pattern = re.compile(r"(?:https?:\/\/)?(?:www\.)?(?:youtu\.be\/|youtube\.com\/watch\?v=)([\w-]+)")
    match = youtube_pattern.match(text)
    return bool(match)
