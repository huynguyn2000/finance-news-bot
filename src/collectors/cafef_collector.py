# src/collectors/cafef_collector.py
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CafeFCollector:
    def __init__(self):
        self.base_url = "https://cafef.vn"
        self.stock_news_url = "https://cafef.vn/thi-truong-chung-khoan.chn"
        
    def get_page_content(self, url):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            print(response.text)
            return response.text
        except Exception as e:
            logger.error(f"Error fetching {url}: {str(e)}")
            return None

    def parse_news_item(self, article):
        try:
            # Lấy link và title
            link_element = article.find('a')
            if not link_element:
                return None
                
            title = link_element.get('title', '').strip()
            link = link_element.get('href', '')
            if link and not link.startswith('http'):
                link = self.base_url + link
                
            # Lấy description
            description = article.find('p', class_='sapo')
            description = description.text.strip() if description else ''
            
            # Lấy thời gian
            time_element = article.find('span', class_='time')
            time_str = time_element.text.strip() if time_element else ''
            
            return {
                'title': title,
                'link': link,
                'description': description,
                'time': time_str,
                'source': 'cafef'
            }
        except Exception as e:
            logger.error(f"Error parsing article: {str(e)}")
            return None

    def collect_news(self):
        content = self.get_page_content(self.stock_news_url)
        if not content:
            return []
            
        soup = BeautifulSoup(content, 'html.parser')
        news_list = soup.find_all('article', class_='news-item')
        
        results = []
        for article in news_list:
            news_item = self.parse_news_item(article)
            if news_item:
                results.append(news_item)
                
        return results

# Test crawler
if __name__ == "__main__":
    collector = CafeFCollector()
    news = collector.collect_news()
    
    # In kết quả
    for item in news:
        print("\n---NEWS ITEM---")
        print(f"Title: {item['title']}")
        print(f"Link: {item['link']}")
        print(f"Description: {item['description']}")
        print(f"Time: {item['time']}")