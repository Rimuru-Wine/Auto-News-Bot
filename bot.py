import aiohttp
import asyncio
import os
import pymongo
import feedparser
from bs4 import BeautifulSoup
import yt_dlp
import logging
import threading
from datetime import datetime

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from config import *
from webhook import start_webhook
from module.rss.rss import format_rss_entry, extract_youtube_watch_url

# ─── Logging ───
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("TeamWineNewsBot")

# ─── Database ───
mongo_client = pymongo.MongoClient(MONGO_URI)
db = mongo_client["TeamWineNewsBot"]
user_settings_collection = db["user_settings"]
global_settings_collection = db["global_settings"]
rss_collection = db["rss_feeds"]

# ─── Pyrogram Client ───
app = Client("TeamWineNewsBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# ─── Webhook Thread ───
threading.Thread(target=start_webhook, daemon=True).start()

# ─── Utility Functions ───
async def send_message(chat_id: int, text: str = None, photo: str = None, video: str = None, reply_markup=None):
    try:
        if photo:
            await app.send_photo(chat_id, photo, caption=text, reply_markup=reply_markup)
        elif video:
            await app.send_video(chat_id, video, caption=text, reply_markup=reply_markup)
        else:
            await app.send_message(chat_id, text, reply_markup=reply_markup)
    except Exception as e:
        logger.error(f"Failed to send message to {chat_id}: {e}")

async def fetch_html(url: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return await resp.text()

async def extract_youtube_video(soup: BeautifulSoup, position: int):
    yt_iframe = soup.find("iframe", src=lambda s: s and ("youtube.com" in s or "youtube-nocookie.com" in s))
    if not yt_iframe:
        return None

    yt_url = yt_iframe["src"]
    if yt_url.startswith("//"):
        yt_url = "https:" + yt_url
    elif yt_url.startswith("/"):
        yt_url = "https://www.youtube.com" + yt_url
    yt_url = extract_youtube_watch_url(yt_url)

    video_path = None
    ydl_opts = {
        "format": "bestvideo[height<=1080]+bestaudio/best[height<=1080]",
        "outtmpl": f"/tmp/ytvideo_{position}.%(ext)s",
        "quiet": True,
        "merge_output_format": "mp4",
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(yt_url, download=True)
            video_path = ydl.prepare_filename(info)
    except Exception as e:
        logger.error(f"Error downloading YouTube video: {e}")
    return video_path

# ─── Commands ───
@app.on_message(filters.command("start"))
async def start(client, message):
    chat_id = message.chat.id
    username = message.from_user.username or "there"

    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("ᴍᴀɪɴ ʜᴜʙ", url="https://t.me/Team_Wine"),
         InlineKeyboardButton("ꜱᴜᴩᴩᴏʀᴛ ᴄʜᴀɴɴᴇʟ", url="https://t.me/Rimuru_wine")],
        [InlineKeyboardButton("ᴅᴇᴠᴇʟᴏᴩᴇʀ", url="https://t.me/Rimuru_wine")]
    ])

    caption = (
        f"<b><blockquote>ʙᴀᴋᴋᴀᴀᴀ {username}!!!\n\n"
        f"I am Team Wine 🍷 Anime News Bot.\n"
        f"I fetch anime news from RSS feeds and automatically post to Team Wine 🍷 news channel.</b></blockquote>"
    )

    await send_message(chat_id, text=caption, photo=START_PIC, reply_markup=buttons if START_PIC else None)

@app.on_message(filters.command("news"))
async def set_news_channel(client, message):
    chat_id = message.chat.id
    if message.from_user.id not in ADMINS:
        await send_message(chat_id, "<b>You do not have permission to use this command.</b>")
        return

    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await send_message(chat_id, "<b>Please provide a channel ID or username.</b>")
        return

    channel_input = args[1].strip()
    channel = int(channel_input) if channel_input.startswith("-100") else f"@{channel_input.lstrip('@')}"
    
    global_settings_collection.update_one({"_id": "config"}, {"$set": {"news_channel": channel}}, upsert=True)
    await send_message(chat_id, f"<b>News channel set to: {channel}</b>")

@app.on_message(filters.command("addrss"))
async def add_rss_feed(client, message):
    chat_id = message.chat.id
    if message.from_user.id not in ADMINS:
        await send_message(chat_id, "<b>You do not have permission to use this command.</b>")
        return

    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await send_message(chat_id, "<b>Usage: /addrss {rss link}</b>")
        return

    rss_link = args[1].strip()
    rss_collection.update_one({"link": rss_link}, {"$set": {"link": rss_link}}, upsert=True)
    await send_message(chat_id, f"<b>RSS feed added: {rss_link}</b>")

@app.on_message(filters.command("listrss"))
async def list_rss(client, message):
    chat_id = message.chat.id
    feeds = list(rss_collection.find({}))
    if not feeds:
        await send_message(chat_id, "<b>No RSS feeds found.</b>")
        return
    text = "<b>Registered RSS feeds:</b>\n" + "\n".join(f"- {f['link']}" for f in feeds)
    await send_message(chat_id, text)

# ─── Auto News Loop ───
async def auto_news_loop():
    await app.wait_until_ready()
    while True:
        try:
            config = global_settings_collection.find_one({"_id": "config"})
            if not config or "news_channel" not in config:
                logger.warning("No news channel configured.")
                await asyncio.sleep(300)
                continue

            news_channel = config["news_channel"]
            feeds = list(rss_collection.find({}))
            for feed_data in feeds:
                rss_link = feed_data["link"]
                feed = feedparser.parse(rss_link)
                if not feed.entries:
                    continue

                for position, entry in enumerate(feed.entries):
                    entry_id = entry.id if 'id' in entry else entry.link
                    if rss_collection.find_one({"link": rss_link, "entry_id": entry_id}):
                        continue

                    msg, thumbnail_url, link = await format_rss_entry(entry)
                    await send_message(news_channel, text=msg, photo=thumbnail_url)

                    try:
                        html = await fetch_html(link)
                        soup = BeautifulSoup(html, "html.parser")
                        video_path = await extract_youtube_video(soup, position)
                        if video_path:
                            await send_message(news_channel, video=video_path, text=f"<b>{entry.title}</b>")
                            os.remove(video_path)
                    except Exception as e:
                        logger.error(f"Error processing video: {e}")

                    rss_collection.update_one(
                        {"link": rss_link, "entry_id": entry_id},
                        {"$set": {"posted_at": datetime.utcnow()}},
                        upsert=True
                    )
            await asyncio.sleep(900)  # wait 15 min between fetches
        except Exception as e:
            logger.error(f"Error in auto_news_loop: {e}")
            await asyncio.sleep(60)

# ─── Run bot and news loop ───
async def main():
    asyncio.create_task(auto_news_loop())
    await app.run()

if __name__ == "__main__":
    asyncio.run(main())
