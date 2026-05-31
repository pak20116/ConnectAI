import os
import requests
import json
import time
import sys
from typing import Optional, Union
from pathlib import Path

# Windows 콘솔에서 한국어 및 이모지 출력을 위해 인코딩 재설정
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if sys.stderr and hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")


# 텔레그램 봇 토큰과 채팅 ID 설정
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "8732529778:AAE-iEa574wM59_uCW8zg2V8MhkfWVxnMMY")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "8986647574")

def send_telegram_message(message: str, token: str = TELEGRAM_BOT_TOKEN, chat_id: str = TELEGRAM_CHAT_ID) -> Optional[dict]:
    """
    텔레그램 봇을 통해 텍스트 메시지를 전송합니다.
    """
    if not token or not chat_id:
        print("Error: 텔레그램 봇 토큰과 챗 ID가 설정되지 않았습니다.")
        return None

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"
    }
    
    try:
        response = requests.post(url, json=payload, timeout=15)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"텔레그램 메시지 전송 실패: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"응답: {e.response.text}")
        return None

def send_telegram_document(file_path: str, caption: str = "", token: str = TELEGRAM_BOT_TOKEN, chat_id: str = TELEGRAM_CHAT_ID) -> Optional[dict]:
    """
    텔레그램 봇을 통해 산출물(파일)을 전송합니다.
    """
    if not token or not chat_id:
        print("Error: 텔레그램 봇 토큰과 챗 ID가 설정되지 않았습니다.")
        return None

    if not os.path.exists(file_path):
        print(f"Error: 파일을 찾을 수 없습니다: {file_path}")
        return None

    url = f"https://api.telegram.org/bot{token}/sendDocument"
    
    try:
        with open(file_path, 'rb') as f:
            files = {'document': f}
            data = {'chat_id': chat_id, 'caption': caption}
            response = requests.post(url, data=data, files=files, timeout=30)
            response.raise_for_status()
            return response.json()
    except requests.exceptions.RequestException as e:
        print(f"텔레그램 파일 전송 실패: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"응답: {e.response.text}")
        return None

def watch_sessions_and_reports(poll_interval: int = 5):
    """
    _company/sessions 폴더와 에이전트 폴더들을 모니터링하여,
    .md, .py, .json 등의 소스/보고서 파일을 제외한 새로운 산출물 파일이 생성되거나 수정되면 자동으로 텔레그램으로 보냅니다.
    """
    company_dir = Path(__file__).resolve().parent.parent
    sessions_dir = company_dir / "sessions"
    agents_dir = company_dir / "_agents"
    
    history_file = Path(__file__).resolve().parent / "telegram_sent_history.json"
    
    # 제외할 확장자 목록 (.md 파일 및 소스코드, 설정파일 등)
    EXCLUDED_EXTENSIONS = {'.md', '.py', '.pyc', '.json', '.jsonl', '.gitkeep', '.gitignore'}
    
    # 이전 전송 이력 로드
    history = {}
    if history_file.exists():
        try:
            with open(history_file, "r", encoding="utf-8") as f:
                history = json.load(f)
        except Exception:
            pass
            
    print("="*60)
    print(f"👀 산출물 자동 전송 모니터링 시작 (주기: {poll_interval}초)...")
    print(f"   (주의: .md, .py, .json 파일은 전송에서 제외됩니다)")
    print(f"   - 감시 대상 1 (세션 폴더): {sessions_dir}")
    print(f"   - 감시 대상 2 (에이전트 폴더): {agents_dir}")
    print(f"   - 전송 이력 파일: {history_file}")
    print("="*60)
    
    while True:
        try:
            files_to_check = []
            
            # 1. sessions 폴더 내의 모든 파일 검색
            if sessions_dir.exists():
                files_to_check.extend(sessions_dir.glob("**/*"))
            
            # 2. 에이전트 폴더 내의 모든 파일 검색
            if agents_dir.exists():
                files_to_check.extend(agents_dir.glob("**/*"))
                
            for filepath in files_to_check:
                # 디렉토리이거나 제외된 확장자인 경우 건너뜀
                if not filepath.is_file() or filepath.suffix.lower() in EXCLUDED_EXTENSIONS:
                    continue
                    
                path_str = str(filepath.resolve())
                
                # 파일 메타데이터 확인
                stat = filepath.stat()
                mtime = stat.st_mtime
                file_size = stat.st_size
                
                # 빈 파일은 제외
                if file_size == 0:
                    continue
                    
                # 이력 확인
                record = history.get(path_str)
                is_new_or_modified = False
                
                if not record:
                    is_new_or_modified = True
                else:
                    # 마지막 전송 시점보다 수정 시각이 1초 이상 최신이거나 파일 크기가 달라진 경우
                    if mtime > record.get("mtime", 0) + 1.0 or file_size != record.get("size", 0):
                        is_new_or_modified = True
                        
                if is_new_or_modified:
                    # 파일 쓰기가 완료될 때까지 대기 (마지막 수정 후 최소 3초 경과 확인)
                    if time.time() - mtime < 3.0:
                        continue
                        
                    # 텔레그램으로 보낼 캡션 제목 작성
                    parts = filepath.parts
                    caption = "📄 새 산출물이 감지되었습니다."
                    
                    if "sessions" in parts:
                        idx = parts.index("sessions")
                        if idx + 2 < len(parts):
                            session_id = parts[idx+1]
                            filename = "/".join(parts[idx+2:])
                            caption = f"📄 [{session_id}] {filename} 생성/수정됨"
                        elif idx + 1 < len(parts):
                            caption = f"📄 [세션] {parts[-1]}"
                    elif "_agents" in parts:
                        idx = parts.index("_agents")
                        if idx + 1 < len(parts):
                            agent_name = parts[idx+1]
                            caption = f"🤖 [{agent_name} 에이전트] {parts[-1]}"
                            
                    print(f"📤 새 산출물 전송 중: {path_str} ({caption})")
                    res = send_telegram_document(path_str, caption=caption)
                    
                    if res:
                        print("✅ 전송 성공")
                        history[path_str] = {
                            "mtime": mtime,
                            "size": file_size,
                            "sent_at": time.strftime('%Y-%m-%d %H:%M:%S')
                        }
                        # 이력 저장
                        with open(history_file, "w", encoding="utf-8") as f:
                            json.dump(history, f, ensure_ascii=False, indent=2)
                    else:
                        print("❌ 전송 실패 (다음 루프에서 재시도)")
                        
        except Exception as e:
            print(f"⚠️ 모니터링 중 에러 발생: {e}")
            
        time.sleep(poll_interval)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "watch":
        watch_sessions_and_reports()
    else:
        print("💡 사용법:")
        print("  - 백그라운드 모니터링 실행: python telegram_notifier.py watch")
        print("  - 파이썬 코드에서 함수 호출:")
        print("      from telegram_notifier import send_telegram_document")
        print("      send_telegram_document('파일경로', '설명')")
