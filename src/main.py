#!/usr/bin/env python3
"""
회사 뉴스 모니터링 봇
"""

import sys
import time
from pathlib import Path

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import config
from src.crawler import NewsCrawler
from src.storage import ArticleStorage
from src.notifier import TelegramNotifier


def main():
    """메인 실행 함수"""
    
    print("=" * 60)
    print("🤖 회사 뉴스봇 시작")
    print("=" * 60)
    
    # 1. 초기화
    print("\n[1/5] 초기화 중...")
    
    if not config.TELEGRAM_BOT_TOKEN or not config.TELEGRAM_CHAT_ID:
        print("❌ 텔레그램 설정이 없습니다!")
        print("   GitHub Secrets에 TELEGRAM_BOT_TOKEN과 TELEGRAM_CHAT_ID를 설정하세요.")
        return 1
    
    crawler = NewsCrawler(
        client_id=config.NAVER_CLIENT_ID,
        client_secret=config.NAVER_CLIENT_SECRET
    )
    storage = ArticleStorage(config.STORAGE_FILE)
    notifier = TelegramNotifier(
        bot_token=config.TELEGRAM_BOT_TOKEN,
        chat_id=config.TELEGRAM_CHAT_ID
    )
    
    # 텔레그램 연결 테스트
    if not notifier.test_connection():
        print("❌ 텔레그램 봇 연결 실패!")
        return 1
    
    for kw in config.SEARCH_KEYWORDS:
        label = ' + '.join(kw) if isinstance(kw, list) else kw
        print(f"  🔑 {label}")

    # 2. 뉴스 크롤링
    print(f"\n[2/5] '{config.COMPANY_NAME}' 뉴스 검색 중...")

    all_articles = []
    for keyword in config.SEARCH_KEYWORDS:
        articles = crawler.search_news(
            keyword=keyword,
            display=config.MAX_ARTICLES_PER_RUN
        )
        all_articles.extend(articles)
        time.sleep(0.5)
    
    if not all_articles:
        print("⚠️  검색 결과가 없습니다.")
        return 0
    
    # 중복 제거
    unique_articles = {article['link']: article for article in all_articles}
    all_articles = list(unique_articles.values())
    
    print(f"📰 총 {len(all_articles)}개 기사 발견")
    
    # 3. 최근 기사만 필터링
    print(f"\n[3/5] 최근 {config.CHECK_INTERVAL_HOURS}시간 내 기사 필터링 중...")
    
    recent_articles = crawler.filter_recent(
        all_articles,
        hours=config.CHECK_INTERVAL_HOURS
    )
    
    if not recent_articles:
        print(f"⚠️  최근 {config.CHECK_INTERVAL_HOURS}시간 내 새 기사가 없습니다.")
        return 0
    
    # 4. 새 기사만 필터링
    print(f"\n[4/5] 새 기사 필터링 중...")
    
    new_articles = []
    skipped_count = 0
    
    for article in recent_articles:
        if not storage.is_sent(article['link']):
            new_articles.append(article)
        else:
            skipped_count += 1
    
    print(f"📨 새 기사: {len(new_articles)}개")
    print(f"⏭️  건너뜀: {skipped_count}개 (이미 전송)")
    
    if not new_articles:
        print("✅ 보낼 새 기사가 없습니다.")
        return 0
    
    # 5. 텔레그램 전송
    print(f"\n[5/5] 텔레그램 전송 중...")
    
    sent_count = 0
    failed_count = 0
    
    for i, article in enumerate(new_articles, 1):
        print(f"\n[{i}/{len(new_articles)}] 전송 중...")
        
        success = notifier.send_article(article)
        
        if success:
            storage.mark_as_sent(article['link'])
            sent_count += 1
        else:
            failed_count += 1
        
        if i < len(new_articles):
            time.sleep(1)
    
    # 요약 전송
    if sent_count > 0:
        notifier.send_summary(
            total=len(recent_articles),
            sent=sent_count,
            skipped=skipped_count
        )
    
    # 6. 정리
    print(f"\n[정리] 오래된 기록 삭제 중...")
    storage.cleanup_old(days=7)
    
    # 7. 결과 출력
    print("\n" + "=" * 60)
    print("📊 실행 결과")
    print("=" * 60)
    print(f"✅ 성공: {sent_count}개")
    print(f"❌ 실패: {failed_count}개")
    print(f"⏭️  건너뜀: {skipped_count}개")
    print("=" * 60)
    
    return 0


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⚠️  사용자에 의해 중단되었습니다.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 예상치 못한 오류: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
