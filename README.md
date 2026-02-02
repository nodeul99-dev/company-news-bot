# 🤖 회사 뉴스 모니터링 봇 v2

회사 관련 뉴스를 자동으로 검색하여 텔레그램으로 알려주는 봇입니다.

## ✨ 주요 기능

- 📰 네이버 뉴스 자동 검색
- ⏰ 매시간 자동 실행 (GitHub Actions)
- 📱 텔레그램 즉시 알림
- 🔄 중복 방지
- 🆓 완전 무료

## 🚀 빠른 시작

### 1. 텔레그램 봇 생성

1. [@BotFather](https://t.me/botfather) 검색
2. `/newbot` 명령으로 봇 생성
3. 봇 토큰 저장

**Chat ID 확인:**
```
봇에게 메시지 보낸 후
https://api.telegram.org/bot<토큰>/getUpdates
에서 "chat":{"id":숫자} 확인
```

### 2. GitHub 레포지토리 생성

1. GitHub에서 새 레포 생성
2. 이 코드 업로드

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <your-repo-url>
git branch -M main
git push -u origin main
```

### 3. GitHub Secrets 설정

**Settings → Secrets and variables → Actions → New repository secret**

필수:
- `TELEGRAM_BOT_TOKEN`: 봇 토큰
- `TELEGRAM_CHAT_ID`: Chat ID

선택 (없으면 웹 크롤링):
- `NAVER_CLIENT_ID`
- `NAVER_CLIENT_SECRET`

### 4. 회사명 설정

`config.py` 파일에서:
```python
COMPANY_NAME = "한국투자증권"  # 여기 수정!
```

### 5. 완료! 🎉

**Actions → Run workflow**로 테스트 실행

## 📁 프로젝트 구조

```
company-news-bot-v2/
├── .github/workflows/monitor.yml
├── src/
│   ├── main.py
│   ├── crawler.py
│   ├── notifier.py
│   └── storage.py
├── data/sent_articles.json
├── config.py
├── requirements.txt
└── README.md
```

## ⚙️ 설정

`config.py`에서 수정 가능:

```python
COMPANY_NAME = "회사명"
CHECK_INTERVAL_HOURS = 1  # 체크 간격
MAX_ARTICLES_PER_RUN = 20  # 검색 개수
```

## ⏰ 실행 주기 변경

`.github/workflows/monitor.yml`:

```yaml
schedule:
  - cron: '0 * * * *'  # 매시간
  # - cron: '0 9,18 * * *'  # 오전9시, 오후6시
```

## 🐛 문제 해결

### 봇이 작동하지 않아요
- Actions 탭에서 로그 확인
- Secrets 설정 확인
- 토큰과 Chat ID 재확인

### 같은 기사가 계속 와요
- `data/sent_articles.json` 커밋 확인

## 🔐 보안

- `.env` 파일은 Git에 커밋 금지
- GitHub Secrets 사용
- 봇 토큰 주기적 재발급 권장

## 📝 라이센스

MIT License

---

**Made with ❤️ for automation**
