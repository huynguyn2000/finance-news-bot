# src/bot.py
from telegram.ext import ApplicationBuilder, CommandHandler
import logging
import os

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Command handlers
async def start(update, context):
    welcome_msg = """
🤖 Chào mừng đến với Finance News Bot!

Các lệnh có sẵn:
/news - Xem tin tức mới nhất
/crypto - Xem tin tiền điện tử
/stocks - Xem tin chứng khoán
/help - Xem hướng dẫn sử dụng
    """
    await update.message.reply_text(welcome_msg)

async def help(update, context):
    help_msg = """
📚 Hướng dẫn sử dụng:

/news - Tin tức tài chính mới nhất
/crypto - Tin về cryptocurrency
/stocks - Tin thị trường chứng khoán
/summary - Tóm tắt thị trường hôm nay
    """
    await update.message.reply_text(help_msg)

async def news(update, context):
    await update.message.reply_text("🔄 Đang tổng hợp tin tức...")
    # Sẽ thêm logic lấy tin tức sau

def main():
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not token:
        logger.error("No token provided!")
        return

    app = ApplicationBuilder().token(token).build()

    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help))
    app.add_handler(CommandHandler("news", news))

    logger.info("Bot started!")
    app.run_polling()

if __name__ == '__main__':
    main()