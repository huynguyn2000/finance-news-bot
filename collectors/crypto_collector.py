# src/collectors/crypto_collector.py
import requests
import logging
import os
from datetime import datetime
from cache.redis_cache import RedisCache

logger = logging.getLogger(__name__)


class CryptoCollector:
    def __init__(self):
        self.api_url = "https://cryptocurrency-news2.p.rapidapi.com/v1/coindesk"
        self.headers = {
            "X-RapidAPI-Host": "cryptocurrency-news2.p.rapidapi.com",
            "X-RapidAPI-Key": os.getenv('RAPIDAPI_KEY')
        }
        self.cache = RedisCache()
        self.cache_key = "crypto_news"
        self.cache_time = 30  # minutes

    async def collect_news(self, limit=5):
        try:
            # Try to get from cache first
            cached_news = await self.cache.get(self.cache_key)
            if cached_news:
                logger.info("Retrieved crypto news from cache")
                return cached_news[:limit]

            # If not in cache, call API
            logger.info("Calling Crypto News API")
            response = requests.get(
                self.api_url,
                headers=self.headers
            )
            response.raise_for_status()

            data = response.json()
            news_items = []

            for item in data['data'][:10]:  # Cache 10 items
                news_items.append({
                    'title': item.get('title'),
                    'url': item.get('url'),
                    'time': item.get('published_at'),
                    'description': item.get('description'),
                    'source': 'coindesk'
                })

            # Save to cache
            await self.cache.set(
                self.cache_key,
                news_items,
                expire_minutes=self.cache_time
            )

            return news_items[:limit]

        except Exception as e:
            logger.error(f"Error collecting crypto news: {e}")
            return []