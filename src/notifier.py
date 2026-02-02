import requests

class TelegramNotifier:
    """텔레그램 메시지 전송 (requests 사용)"""
    
    def __init__(self, bot_token, chat_id):
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.base_url = f"https://api.telegram.org/bot{bot_token}"
    
    def send_article(self, article):
        """기사를 텔레그램으로 전송"""
        try:
            message = self._format_message(article)
            
            url = f"{self.base_url}/sendMessage"
            data = {
                'chat_id': self.chat_id,
                'text': message,
                'parse_mode': 'Markdown',
                'disable_web_page_preview': False
            }
            
            response = requests.post(url, json=data, timeout=10)
            response.raise_for_status()
            
            print(f"✅ 전송 완료: {article['title'][:30]}...")
            return True
            
        except Exception as e:
            print(f"❌ 전송 실패: {e}")
            return False
    
    def _format_message(self, article):
        """메시지 포맷팅"""
        title = article.get('title', '제목 없음')
        description = article.get('description', '')
        link = article.get('link', '')
        source = article.get('source', '출처 미상')
        pub_date = article.get('pubDate', '')
        
        # 날짜 포맷팅
        if hasattr(pub_date, 'strftime'):
            date_str = pub_date.strftime('%Y-%m-%d %H:%M')
        else:
            date_str = str(pub_date)
        
        # 메시지 구성
        message = f"""🔔 *새 뉴스 발견*

*{self._escape_markdown(title)}*

{self._escape_markdown(description[:200])}{'...' if len(description) > 200 else ''}

📰 출처: {self._escape_markdown(source)}
⏰ {date_str}

🔗 [기사 보기]({link})
"""
        return message
    
    def _escape_markdown(self, text):
        """Markdown 특수문자 이스케이프"""
        special_chars = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
        for char in special_chars:
            text = text.replace(char, f'\\{char}')
        return text
    
    def send_summary(self, total, sent, skipped):
        """실행 요약 전송"""
        try:
            message = f"""📊 *뉴스봇 실행 완료*

• 발견: {total}개
• 전송: {sent}개
• 건너뜀: {skipped}개 (중복)
"""
            
            url = f"{self.base_url}/sendMessage"
            data = {
                'chat_id': self.chat_id,
                'text': message,
                'parse_mode': 'Markdown'
            }
            
            response = requests.post(url, json=data, timeout=10)
            response.raise_for_status()
            return True
            
        except Exception as e:
            print(f"⚠️  요약 전송 실패: {e}")
            return False
    
    def test_connection(self):
        """봇 연결 테스트"""
        try:
            url = f"{self.base_url}/getMe"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            if data.get('ok'):
                bot_info = data.get('result', {})
                username = bot_info.get('username', 'Unknown')
                print(f"✅ 텔레그램 봇 연결 성공: @{username}")
                return True
            else:
                print(f"❌ 텔레그램 봇 연결 실패")
                return False
                
        except Exception as e:
            print(f"❌ 텔레그램 봇 연결 실패: {e}")
            return False
