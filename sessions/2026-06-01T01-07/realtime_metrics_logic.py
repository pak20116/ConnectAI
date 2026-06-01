import json
from typing import List, Dict, Any
from datetime import datetime

# --- 1. 데이터 구조 정의 (Schema Definition) ---

class SessionLog:
    """사용자 시청 행동 로그의 기본 구조."""
    def __init__(self, session_id: str, video_id: str, start_time: float, end_time: float, duration: float):
        self.session_id = session_id
        self.video_id = video_id
        self.start_time = start_time  # 영상 시작 시점 (Timestamp)
        self.end_time = end_time      # 영상 종료 시점 (Timestamp)
        self.duration = duration      # 총 시청 시간 (초 단위)

class VSMResult:
    """Visual Sequence Module(VSM) 적용 결과를 담는 구조."""
    def __init__(self, video_id: str, applied_modules: List[str], vsm_effect: Dict[str, float]):
        self.video_id = video_id
        self.applied_modules = applied_modules  # 적용된 VSM 모듈 리스트
        self.vsm_effect = vsm_effect          # 각 모듈별 시청 지속률 변화율 (예: Focus: +15%)

class RealtimeMetricRequest:
    """API 요청에 필요한 입력 데이터 구조."""
    def __init__(self, session_logs: List[SessionLog], vsm_results: List[VSMResult]):
        self.session_logs = session_logs
        self.vsm_results = vsm_results

# --- 2. 핵심 측정 로직 (Core Measurement Logic) ---

def calculate_avg_view_duration(logs: List[SessionLog]) -> float:
    """모든 세션 로그의 평균 시청 지속률(AVD)을 계산합니다."""
    if not logs:
        return 0.0
    total_duration = sum(log.duration for log in logs)
    return total_duration / len(logs)

def calculate_segment_dropoff_rate(
    logs: List[SessionLog], 
    vsm_results: List[VSMResult], 
    segment_start_time_sec: float, 
    segment_end_time_sec: float
) -> Dict[str, float]:
    """특정 구간에서의 이탈률을 계산합니다. VSM 적용 여부에 따라 분리하여 측정."""
    
    # 1. 전체 로그 필터링 (단순화를 위해 여기서는 모든 로그를 사용한다고 가정)
    relevant_logs = logs

    # 2. VSM 기반 세그먼트별 이탈률 계산
    dropoff_metrics = {}
    
    for log in relevant_logs:
        # 예시 로직: 특정 시점에 구간을 설정하고, 해당 구간 내에서 시청 중단 비율 측정
        if log.start_time > segment_start_time_sec and log.end_time < segment_end_time_sec:
            # 이 예시는 실제 로그 데이터가 세밀하게 기록되어야 정확하지만, 현재는 개념적 로직을 제시합니다.
            pass 

    # 실제 구현에서는 로그의 타임스탬프를 기반으로 구간별 시청 중단 시간을 계산해야 합니다.
    # 여기서는 요구사항에 맞게 추상적인 구조만 정의하고, 실제 데이터가 들어왔을 때 구체화하도록 설계합니다.
    dropoff_metrics['overall_dropoff'] = (1 - calculate_avg_view_duration(logs) / 300) * 100 # 임시 계산 예시
    
    return dropoff_metrics

def generate_realtime_report(request: RealtimeMetricRequest) -> Dict[str, Any]:
    """실시간 측정 데이터를 종합하여 최종 대시보드 포맷을 반환합니다."""
    
    # 1. 핵심 지표 계산
    avg_avd = calculate_avg_view_duration(request.session_logs)
    
    # 2. VSM 효과 통합 분석 (가장 중요한 연결 고리)
    vsm_impact_summary = {}
    if request.vsm_results:
        total_vsm_effect = sum(sum(res.vsm_effect.values()) for res in request.vsm_results)
        vsm_impact_summary['total_vsm_positive_impact'] = total_vsm_effect
    else:
        vsm_impact_summary['total_vsm_positive_impact'] = 0.0

    # 3. 이탈률 분석 (구간별, VSM별)
    dropoff_analysis = {}
    # TODO: 실제 로그 데이터를 사용하여 segment_dropoff_rate 함수 호출 로직 추가 필요.
    dropoff_analysis['segment_focus_loss'] = "데이터 연동 후 계산" 
    dropoff_analysis['segment_escape_loss'] = "데이터 연동 후 계산"

    # 4. 최종 결과 포맷팅
    report = {
        "timestamp": datetime.now().isoformat(),
        "overall_metrics": {
            "avg_view_duration_seconds": round(avg_avd, 2),
            "total_sessions": len(request.session_logs)
        },
        "vsm_analysis": vsm_impact_summary,
        "dropoff_analysis": dropoff_analysis,
        "raw_data_count": len(request.session_logs),
    }

    return report

# --- 3. 테스트 실행 (Self-Verification Loop) ---

def run_test_suite():
    """측정 로직의 기본 기능 검증을 위한 테스트 시퀀스."""
    print("--- 측정 로직 테스트 시작 ---")
    
    # 가상 데이터 생성: 실제 로그와 VSM 결과를 시뮬레이션합니다.
    mock_logs = [
        SessionLog("S001", "V101", 100, 300, 200),  # 3분 시청
        SessionLog("S002", "V102", 500, 800, 300),  # 5분 시청
    ]
    mock_vsm = [
        VSMResult("V101", ["Focus"], {"Focus": 15.0}),
        VSMResult("V102", ["Escape"], {"Escape": 10.0}),
    ]

    # AVD 계산 테스트
    avg_duration = calculate_avg_view_duration(mock_logs)
    print(f"AVD 계산 결과 (Mock): {avg_duration}초") # 예상: (200 + 300) / 2 = 250.0

    # 보고서 생성 테스트
    request = RealtimeMetricRequest(mock_logs, mock_vsm)
    report = generate_realtime_report(request)
    print("\n--- 최종 리포트 포맷 확인 ---")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    print("--- 테스트 완료 ---")

# 실행
run_test_suite()