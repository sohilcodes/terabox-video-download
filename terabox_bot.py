import logging
import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = "7874902019:AAHBesixmA4duXQCo9t7C1sR2pVg8nZ0P9I"  # Replace with your Telegram bot token

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send me a Terabox video URL and I'll get you the direct download link.")

def get_terabox_direct_link(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")
        
        # Terabox usually uses a videoPlayer script; this may vary.
        for script in soup.find_all("script"):
            if "videoPlayer" in script.text and "https://" in script.text:
                start = script.text.find("https://")
                end = script.text.find(".mp4") + 4
                direct_url = script.text[start:end]
                return direct_url
        return None
    except Exception as e:
        print("Error:", e)
        return None

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    if "terabox" not in url:
        await update.message.reply_text("Please send a valid Terabox video URL.")
        return

    await update.message.reply_text("Processing your link...")
    direct_link = get_terabox_direct_link(url)

    if direct_link:
        await update.message.reply_text(f"Here is your direct video link:\n{direct_link}")
    else:
        await update.message.reply_text("Failed to extract video link. It may be private or unsupported.")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()
