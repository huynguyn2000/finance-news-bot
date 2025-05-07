# src/collectors/vnstock_collector.py
import requests
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)


class VNStockCollector:
    def __init__(self):
        self.cafef_url = "https://cafef.vn/thi-truong-chung-khoan.chn"

    async def collect_news(self, limit=5):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }

            response = requests.get(self.cafef_url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')

            news_items = []
            articles = soup.find_all('article', class_='news-item')[:limit]

            for article in articles:
                title = article.find('a').get('title', '').strip()
                link = article.find('a').get('href', '')
                if link and not link.startswith('http'):
                    link = f"https://cafef.vn{link}"

                time = article.find('span', class_='time')
                time = time.text.strip() if time else ''

                description = article.find('p', class_='sapo')
                description = description.text.strip() if description else ''

                news_items.append({
                    'title': title,
                    'url': link,
                    'time': time,
                    'description': description,
                    'source': 'cafef'
                })

            return news_items

        except Exception as e:
            logger.error(f"Error collecting VN stock news: {e}")
            return []