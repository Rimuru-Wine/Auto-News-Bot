import re
from bs4 import BeautifulSoup

async def format_rss_entry(entry):
    """
    Formats an RSS feed entry into message, thumbnail, and link.
    """
    title = getattr(entry, "title", "No Title")
    link = getattr(entry, "link", None)
    summary = getattr(entry, "summary", "")
    
    # Try to extract image from summary
    thumbnail_url = None
    soup = BeautifulSoup(summary, "html.parser")
    img = soup.find("img")
    if img and img.get("src"):
        thumbnail_url = img["src"]
    
    msg = f"<b>{title}</b>\n\n{re.sub('<[^<]+?>', '', summary)}\n\n<a href='{link}'>Read More</a>"
    return msg, thumbnail_url, link

def extract_youtube_watch_url(url):
    """
    Converts embed URL to YouTube watch URL.
    """
    if "embed/" in url:
        video_id = url.split("embed/")[-1].split("?")[0]
        return f"https://www.youtube.com/watch?v={video_id}"
    return url
