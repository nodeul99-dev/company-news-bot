import os
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# 텔레그램 설정 (필수)
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# 회사 정보 (여기를 수정하세요!)
COMPANY_NAME = "한국투자증권"  # 예시 - 실제 회사명으로 변경하세요

# 검색 키워드
SEARCH_KEYWORDS = [COMPANY_NAME]

# 네이버 검색 API (선택사항 - 없으면 웹 크롤링 사용)
NAVER_CLIENT_ID = os.getenv('NAVER_CLIENT_ID', '')
NAVER_CLIENT_SECRET = os.getenv('NAVER_CLIENT_SECRET', '')

# 크롤링 설정
CHECK_INTERVAL_HOURS = 1  # 최근 N시간 내 뉴스만 확인
MAX_ARTICLES_PER_RUN = 20  # 한 번에 최대 검색 개수
STORAGE_FILE = 'data/sent_articles.json'
