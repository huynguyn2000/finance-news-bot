# src/services/news_service.py
from src.bot import logger
from src.collectors.crypto_collector import CryptoCollector
from src.collectors.vnstock_collectors import VNStockCollector

class NewsService:
    def __init__(self):
        self.vn_collector = VNStockCollector()
        self.crypto_collector = CryptoCollector()

    async def get_stock_news(self, limit=5):
        try:
            news_items = await self.vn_collector.collect_news(limit=limit)
            return self._format_news_list(news_items, "Tin thị trường chứng khoán")
        except Exception as e:
            logger.error(f"Error getting stock news: {e}")
            return "❌ Có lỗi xảy ra khi lấy tin chứng khoán!"

    async def get_crypto_news(self, limit=5):
        try:
            news_items = await self.crypto_collector.collect_news(limit=limit)
            return self._format_news_list(news_items, "Tin Crypto")
        except Exception as e:
            logger.error(f"Error getting crypto news: {e}")
            return "❌ Có lỗi xảy ra khi lấy tin crypto!"

    def _format_news_list(self, news_items, title):
        if not news_items:
            return f"Không có tin tức mới về {title}!"

        formatted = f"📰 {title} mới nhất:\n\n"

        for idx, item in enumerate(news_items, 1):
            formatted += f"{idx}. {item['title']}\n"
            formatted += f"⏰ {item['time']}\n"
            if item.get('description'):
                formatted += f"📝 {item['description'][:100]}...\n"
            formatted += f"🔗 {item['url']}\n"
            formatted += f"📰 Nguồn: {item['source']}\n\n"

        return formatted