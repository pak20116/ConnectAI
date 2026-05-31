import os
import requests
import json
from typing import Optional, Union

# 텔레그램 봇 토큰과 채팅 ID를 환경변수에서 가져오거나 직접 설정할 수 있습니다.
# 사용하기 전에 본인의 TOKEN과 CHAT_ID로 변경하거나 환경변수를 설정해주세요.
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "YOUR_CHAT_ID_HERE")

def send_telegram_message(message: str, token: str = TELEGRAM_BOT_TOKEN, chat_id: str = TELEGRAM_CHAT_ID) -> Optional[dict]:
    """
    텔레그램 봇을 통해 텍스트 메시지를 전송합니다.
    """
    if token == "YOUR_BOT_TOKEN_HERE" or chat_id == "YOUR_CHAT_ID_HERE":
        print("Error: 텔레그램 봇 토큰과 챗 ID가 설정되지 않았습니다.")
        return None

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"
    }
    
    try:
        response = requests.post(url, json=payload)
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
    if token == "YOUR_BOT_TOKEN_HERE" or chat_id == "YOUR_CHAT_ID_HERE":
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
            response = requests.post(url, data=data, files=files)
            response.raise_for_status()
            return response.json()
    except requests.exceptions.RequestException as e:
        print(f"텔레그램 파일 전송 실패: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"응답: {e.response.text}")
        return None

# 예시 사용법
if __name__ == "__main__":
    # 테스트 메시지 전송
    # send_telegram_message("🚀 산출물 생성이 완료되었습니다.")
    
    # 특정 파일 전송 예시
    # report_path = r"c:\Users\Sung\ConnectAI\_company\sessions\2026-05-30T22-20\_report.md"
    # send_telegram_document(report_path, caption="📄 최신 리포트 산출물입니다.")
    pass
