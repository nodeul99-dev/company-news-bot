import requests
from datetime import datetime, timedelta
from typing import List, Dict
import re

class NewsCrawler:
    """네이버 뉴스 검색"""
    
    def __init__(self, client_id=None, client_secret=None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.base_url = "https://openapi.naver.com/v1/search/news.json"
    
    def search_news(self, keyword, display=20):
        """네이버 뉴스 검색"""
        if self.client_id and self.client_secret:
            return self._search_with_api(keyword, display)
        else:
            return self._search_with_crawl(keyword, display)
    
    def _search_with_api(self, keyword, display):
        """네이버 API로 검색"""
        try:
            headers = {
                'X-Naver-Client-Id': self.client_id,
                'X-Naver-Client-Secret': self.client_secret
            }
            
            params = {
                'query': keyword,
                'display': min(display, 100),
                'sort': 'date'
            }
            
            response = requests.get(self.base_url, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            articles = []
            
            for item in data.get('items', []):
                article = {
                    'title': self._clean_html(item['title']),
                    'description': self._clean_html(item['description']),
                    'link': item.get('originallink') or item['link'],
                    'pubDate': self._parse_date(item['pubDate']),
                    'source': '네이버 뉴스'
                }
                articles.append(article)
            
            print(f"📰 네이버 API: {len(articles)}개 기사 발견")
            return articles
            
        except Exception as e:
            print(f"⚠️  네이버 API 실패: {e}")
            return self._search_with_crawl(keyword, display)
    
    def _search_with_crawl(self, keyword, display):
        """웹 크롤링으로 검색"""
        try:
            from bs4 import BeautifulSoup
            
            url = "https://search.naver.com/search.naver"
            params = {
                'where': 'news',
                'query': keyword,
                'sort': 0,
                'start': 1
            }
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, params=params, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            articles = []
            
            news_items = soup.select('.news_area')
            
            for item in news_items[:display]:
                try:
                    title_elem = item.select_one('.news_tit')
                    if not title_elem:
                        continue
                    
                    title = title_elem.get_text(strip=True)
                    link = title_elem.get('href', '')
                    
                    desc_elem = item.select_one('.news_dsc')
                    description = desc_elem.get_text(strip=True) if desc_elem else ''
                    
                    info_elem = item.select_one('.info')
                    source = info_elem.get_text(strip=True) if info_elem else '뉴스'
                    
                    article = {
                        'title': title,
                        'description': description,
                        'link': link,
                        'pubDate': datetime.now(),
                        'source': source
                    }
                    articles.append(article)
                    
                except Exception:
                    continue
            
            print(f"📰 웹 크롤링: {len(articles)}개 기사 발견")
            return articles
            
        except Exception as e:
            print(f"❌ 웹 크롤링 실패: {e}")
            return []
    
    def filter_recent(self, articles, hours=1):
        """최근 N시간 내 기사만 필터링"""
        cutoff = datetime.now() - timedelta(hours=hours)
        recent = []
        
        for article in articles:
            pub_date = article.get('pubDate')
            if isinstance(pub_date, datetime) and pub_date > cutoff:
                recent.append(article)
        
        print(f"⏰ 최근 {hours}시간 내: {len(recent)}개")
        return recent
    
    def _clean_html(self, text):
        """HTML 태그 제거"""
        text = re.sub('<[^<]+?>', '', text)
        text = text.replace('&quot;', '"')
        text = text.replace('&apos;', "'")
        text = text.replace('&amp;', '&')
        text = text.replace('&lt;', '<')
        text = text.replace('&gt;', '>')
        return text.strip()
    
    def _parse_date(self, date_str):
        """날짜 문자열을 datetime으로 변환"""
        try:
            from email.utils import parsedate_to_datetime
            return parsedate_to_datetime(date_str)
        except:
            return datetime.now()
