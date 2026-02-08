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
        """네이버 뉴스 검색. keyword가 리스트이면 AND 조건으로 필터링."""
        if isinstance(keyword, list):
            # AND 키워드: 첫 번째 키워드로 검색 후, 모든 키워드가 포함된 기사만 반환
            search_term = keyword[0]
            required_terms = keyword
        else:
            search_term = keyword
            required_terms = None

        if self.client_id and self.client_secret:
            articles = self._search_with_api(search_term, display)
        else:
            articles = self._search_with_crawl(search_term, display)

        if required_terms:
            articles = self._filter_by_all_terms(articles, required_terms)

        return articles

    def _filter_by_all_terms(self, articles, terms):
        """기사 제목+본문에 모든 키워드가 포함된 것만 반환"""
        filtered = []
        for article in articles:
            text = (article.get('title', '') + ' ' + article.get('description', '')).lower()
            if all(term.lower() in text for term in terms):
                filtered.append(article)
        print(f"🔍 AND 필터 ({' + '.join(terms)}): {len(articles)}개 → {len(filtered)}개")
        return filtered
    
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
            if pub_date and pub_date.replace(tzinfo=None) >= cutoff:
                recent.append(article)
        print(f"⏰ 최근 {hours}시간 필터: {len(articles)}개 → {len(recent)}개")
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
