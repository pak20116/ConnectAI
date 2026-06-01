import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# --- 1. 가상 데이터 생성 함수 (실제 환경에서는 DB에서 데이터를 읽어옵니다) ---
def generate_mock_data(num_records=1000):
    """시청 로그 및 시스템 안정성 지표를 모방한 가상 데이터 생성"""
    start_date = datetime(2026, 5, 1)
    data = []
    
    # 시스템 안정성 메트릭 (L_sync, epsilon) - 이 값들은 시스템 상태에 따라 변동한다고 가정
    stability_metrics = np.random.uniform(0.9, 1.0, num_records) # L_sync: 동기화 지표 (1에 가까울수록 안정), epsilon: 오차 범위
    
    for i in range(num_records):
        timestamp = start_date + timedelta(minutes=i*5)
        # 시청 로그 데이터
        view_duration = np.random.uniform(30, 600) # 시청 시간 (초)
        engagement_score = np.random.uniform(0, 100) # 몰입도 점수
        
        data.append({
            'timestamp': timestamp,
            'view_duration_sec': view_duration,
            'engagement_score': engagement_score,
            'L_sync': stability_metrics[i],
            'epsilon': np.random.uniform(0.01, 0.1), # 오차 범위
        })
    return pd.DataFrame(data)

# --- 2. 핵심 집계 로직 구현 ---
def integrate_focus_escape_kpi(df: pd.DataFrame) -> pd.DataFrame:
    """
    시청 행동 로그와 시스템 안정성 메트릭을 통합하여 Focus & Escape KPI를 계산합니다.
    """
    print("⚙️ 데이터 통합 및 KPI 계산 로직 실행 중...")
    
    # 1. 타임스탬프 기반 그룹화 (예: 시간 단위 또는 특정 구간)
    df['time_bucket'] = df['timestamp'].dt.floor('10min') # 10분 단위로 집계하여 노이즈 감소

    # 2. 시스템 안정성 필터링 (안정성이 낮으면 해당 데이터의 가중치를 낮춤)
    # 예시: L_sync가 0.95 미만인 경우, 해당 구간의 지표를 보수적으로 처리하거나 제외
    df['stability_flag'] = np.where(df['L_sync'] < 0.95, 'Low_Stability', 'Stable')

    # 3. Focus & Escape 지표 계산 (핵심 로직)
    # Focus: 높은 몰입도 점수와 긴 시청 시간을 결합
    df['focus_metric'] = df['engagement_score'] * (df['view_duration_sec'] / 60) # 몰입도 x 시간 비율
    
    # Escape: 안정성과 집중도를 고려한 이탈률 추정 (가상의 계산)
    # 안정성이 높을수록, 몰입도가 높을수록 이탈이 적다고 가정
    df['escape_risk'] = (1 - df['engagement_score'] / 100) * (1 - df['L_sync']) # 안정성과 집중도 부족에 따른 위험 지표

    # 4. 최종 KPI 결합
    df['focus_escape_kpi'] = df['focus_metric'] * (1 + (df['L_sync'] * 0.5)) # 안정성이 높을수록 점수 가산 적용

    # 5. 집계 및 요약
    summary = df.groupby('time_bucket').agg(
        avg_focus_escape=pd.NamedAgg(column='focus_escape_kpi', aggfunc='mean'),
        avg_l_sync=pd.NamedAgg(column='L_sync', aggfunc='mean'),
        count=pd.NamedAgg(column='view_duration_sec', aggfunc='count')
    ).reset_index()

    print("✅ 데이터 통합 완료. 요약 결과:")
    print(summary)
    
    return df, summary

# --- 3. 테스트 실행 ---
if __name__ == "__main__":
    print("--- 시스템 안정성 및 행동 로그 통합 테스트 시작 ---")
    
    # 1. 가상 데이터 생성
    mock_df = generate_mock_data(num_records=5000)
    print(f"✅ 가상 데이터 {len(mock_df)}건 생성 완료.")
    
    # 2. KPI 통합 실행
    processed_df, summary_result = integrate_focus_escape_kpi(mock_df)
    
    print("\n--- 최종 요약 결과 (Focus & Escape KPI) ---")
    print(summary_result.to_markdown(index=False))
    
    print("\n💻 테스트 완료.")