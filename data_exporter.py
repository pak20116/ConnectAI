import json
import os
from datetime import datetime

DATA_FILE = "stability_data.json"

def load_kpi_data():
    """stability_data.json 파일에서 모든 KPI 데이터를 로드합니다."""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print("⚠️ 경고: stability_data.json 파일이 손상되었습니다. 빈 리스트 반환.")
        return []

def get_latest_kpi():
    """가장 최근에 기록된 KPI 데이터만 반환합니다."""
    all_data = load_kpi_data()
    if not all_data:
        return None
    # 가장 마지막 항목을 최신 데이터로 간주하고 반환
    return all_data[-1]

def export_kpi_for_salespage():
    """Sales Page에 바로 반영할 수 있도록 핵심 KPI를 추출하여 딕셔너리로 반환합니다."""
    latest = get_latest_kpi()
    if latest:
        # Sales Page가 요구하는 형태로 데이터 포맷팅 (예시)
        return {
            "latency": latest.get("latency_ms"),
            "consistency": latest.get("visual_consistency_score"),
            "timestamp": latest.get("timestamp")
        }
    return None

if __name__ == "__main__":
    kpi = export_kpi_for_salespage()
    if kpi:
        print("--- Sales Page 데이터 추출 성공 ---")
        print(f"Latency_ms: {kpi['latency']}")
        print(f"VisualConsistencyScore: {kpi['consistency']}")
        print(f"Timestamp: {kpi['timestamp']}")
    else:
        print("KPI 데이터를 찾을 수 없습니다.")