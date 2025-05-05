# src/bot.py
import logging
from telegram.ext import ApplicationBuilder, CommandHandler
import os

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update, context):
    await update.message.reply_text('Hello! I am Finance News Bot!')

async def get_news(update, context):
    await update.message.reply_text('Getting latest news...')

def main():
    # Get token from environment variable
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not token:
        logger.error("No token provided!")
        return

    # Create application
    application = ApplicationBuilder().token(token).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("news", get_news))

    # Start bot
    logger.info("Bot started!")
    application.run_polling()

if __name__ == '__main__':
    main()