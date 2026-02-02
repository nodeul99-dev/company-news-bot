import json
import os
from datetime import datetime, timedelta

class ArticleStorage:
    """발송한 기사 이력 관리"""
    
    def __init__(self, storage_file):
        self.storage_file = storage_file
        self.data = {}
        self._ensure_file_exists()
        self._load()
    
    def _ensure_file_exists(self):
        """저장 파일이 없으면 생성"""
        os.makedirs(os.path.dirname(self.storage_file), exist_ok=True)
        if not os.path.exists(self.storage_file):
            with open(self.storage_file, 'w', encoding='utf-8') as f:
                json.dump({}, f)
    
    def _load(self):
        """저장된 데이터 로드"""
        try:
            with open(self.storage_file, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
            print(f"📂 저장된 기사 이력: {len(self.data)}개")
        except Exception as e:
            print(f"⚠️  이력 로드 실패: {e}")
            self.data = {}
    
    def _save(self):
        """데이터 저장"""
        try:
            with open(self.storage_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"⚠️  이력 저장 실패: {e}")
    
    def is_sent(self, article_url):
        """이미 보낸 기사인지 확인"""
        return article_url in self.data
    
    def mark_as_sent(self, article_url):
        """발송 완료로 기록"""
        self.data[article_url] = datetime.now().isoformat()
        self._save()
    
    def cleanup_old(self, days=7):
        """오래된 기록 삭제"""
        cutoff = datetime.now() - timedelta(days=days)
        original_count = len(self.data)
        
        to_remove = []
        for url, timestamp in self.data.items():
            try:
                sent_time = datetime.fromisoformat(timestamp)
                if sent_time < cutoff:
                    to_remove.append(url)
            except:
                to_remove.append(url)
        
        for url in to_remove:
            del self.data[url]
        
        if to_remove:
            self._save()
            print(f"🗑️  {len(to_remove)}개 오래된 기록 삭제")
