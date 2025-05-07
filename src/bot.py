# src/bot.py
from telegram.ext import ApplicationBuilder, CommandHandler
from services.news_service import NewsService
import logging
import os

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


class FinanceNewsBot:
    def __init__(self):
        self.news_service = NewsService()

    async def start(self, update, context):
        welcome_msg = """
🤖 Chào mừng đến với Finance News Bot!

Các lệnh có sẵn:
/news - Xem tin tức tài chính mới nhất
/sentiment - Xem phân tích sentiment thị trường
/help - Xem hướng dẫn sử dụng
        """
        await update.message.reply_text(welcome_msg)

    async def get_news(self, update, context):
        await update.message.reply_text("🔄 Đang tổng hợp tin tức...")
        news = await self.news_service.get_latest_news(limit=5)
        await update.message.reply_text(news, disable_web_page_preview=True)


def main():
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not token:
        logger.error("No token provided!")
        return

    bot = FinanceNewsBot()
    app = ApplicationBuilder().token(token).build()

    # Add handlers
    app.add_handler(CommandHandler("start", bot.start))
    app.add_handler(CommandHandler("news", bot.get_news))

    logger.info("Bot started!")
    app.run_polling()


if __name__ == '__main__':
    main()