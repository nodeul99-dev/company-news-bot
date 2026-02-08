import os
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# 텔레그램 설정 (필수)
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

COMPANY_NAME = "DS투자증권"

# 단독 키워드: 문자열 하나 → 해당 키워드가 포함된 기사 검색
# AND 키워드: 리스트 → 검색은 첫 번째로 하되, 모든 키워드가 기사에 포함된 것만 필터링
SEARCH_KEYWORDS = [
    "DS투자증권",
    "디에스투자증권",
    ["디에스자산운용", "장덕수"],
    ["DS자산운용", "장덕수"],
]

# 네이버 검색 API (선택사항 - 없으면 웹 크롤링 사용)
NAVER_CLIENT_ID = os.getenv('NAVER_CLIENT_ID', '')
NAVER_CLIENT_SECRET = os.getenv('NAVER_CLIENT_SECRET', '')

# 크롤링 설정
CHECK_INTERVAL_HOURS = 6  # 최근 N시간 내 뉴스만 확인
MAX_ARTICLES_PER_RUN = 5  # 한 번에 최대 검색 개수
STORAGE_FILE = 'data/sent_articles.json'
