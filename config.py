import os
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# 텔레그램 설정 (필수)
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

COMPANY_NAME = "DS투자증권"

SEARCH_KEYWORDS = [
    "DS투자증권",
    "디에스투자증권",
    "디에스증권",
    "장덕수 DS",
    "장덕수 디에스"
]

# 네이버 검색 API (선택사항 - 없으면 웹 크롤링 사용)
NAVER_CLIENT_ID = os.getenv('NAVER_CLIENT_ID', '')
NAVER_CLIENT_SECRET = os.getenv('NAVER_CLIENT_SECRET', '')

# 크롤링 설정
CHECK_INTERVAL_HOURS = 1  # 최근 N시간 내 뉴스만 확인
MAX_ARTICLES_PER_RUN = 5  # 한 번에 최대 검색 개수
STORAGE_FILE = 'data/sent_articles.json'
