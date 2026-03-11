import re

def is_youtube_video(url: str) -> bool:
    youtube_regex = r"(https?://)?(www\.)?(youtube\.com|youtu\.be)/(watch\?v=|shorts/|embed/)?([A-Za-z0-9_-]{11})"

    match = re.search(youtube_regex, url)
    return bool(match)