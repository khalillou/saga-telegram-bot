import os
import time
import feedparser
import telegram
from keep_alive import keep_alive

bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
chat_id = os.environ.get("TELEGRAM_CHAT_ID")
rss_url = os.environ.get("RSS_FEED_URL")

bot = telegram.Bot(token=bot_token)
last_entry = None

keep_alive()

while True:
    feed = feedparser.parse(rss_url)
    if not feed.entries:
        print("No entries found.")
        time.sleep(60)
        continue

    new_entry = feed.entries[0]
    if last_entry != new_entry.id:
        message = f"{new_entry.title}\n{new_entry.link}"
        bot.send_message(chat_id=chat_id, text=message)
        last_entry = new_entry.id
        print(f"Sent: {message}")
    else:
        print("No new update.")

    time.sleep(60)
