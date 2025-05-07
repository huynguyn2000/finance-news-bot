# src/cache/redis_cache.py
import redis
import json
import os
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)


class RedisCache:
    def __init__(self):
        self.redis_client = redis.Redis(
            host=os.getenv('REDIS_HOST', 'localhost'),
            port=os.getenv('REDIS_PORT', 6379),
            password=os.getenv('REDIS_PASSWORD', None),
            decode_responses=True
        )

    async def get(self, key):
        try:
            data = self.redis_client.get(key)
            return json.loads(data) if data else None
        except Exception as e:
            logger.error(f"Redis get error: {e}")
            return None

    async def set(self, key, value, expire_minutes=30):
        try:
            self.redis_client.setex(
                key,
                timedelta(minutes=expire_minutes),
                json.dumps(value)
            )
        except Exception as e:
            logger.error(f"Redis set error: {e}")