import pandas as pd
from typing import Optional

def synchronize_and_aggregate_metrics(log_path: str, revenue_path: str) -> Optional[pd.DataFrame]:
    """
    시청 행동 로그와 수익화 데이터를 Timestamp를 기준으로 동기화하고 핵심 KPI를 집계합니다.

    Args:
        log_path: 시청 행동 로그 파일 경로 (예: JSON 또는 CSV)
        revenue_path: 수익화 데이터 파일 경로 (예: JSON 또는 CSV)

    Returns:
        동기화 및 집계된 통합 DataFrame, 실패 시 None
    """
    print(f"🔍 시작: {log_path} 및 {revenue_path} 데이터 동기화 프로세스")
    try:
        # 1. 로그 데이터 로드 (가정: Timestamp 컬럼 존재)
        df_logs = pd.read_json(log_path)
        print(f"✅ {log_path} 로드 완료. 행 수: {len(df_logs)}")

        # 2. 수익화 데이터 로드 (가정: Timestamp 및 수익 정보 컬럼 존재)
        df_revenue = pd.read_json(revenue_path)
        print(f"✅ {revenue_path} 로드 완료. 행 수: {len(df_revenue)}")

        # 3. Timestamp를 기준으로 데이터 정렬 (가장 중요)
        # 로그 데이터는 시청 시작/종료 타임스탬프, 수익화 데이터는 발생 시점을 기준으로 병합
        if 'timestamp' not in df_logs.columns or 'timestamp' not in df_revenue.columns:
            print("❌ 오류: 필수 컬럼 'timestamp'가 로그 또는 수익화 데이터에 존재하지 않습니다. 스키마를 확인해주세요.")
            return None

        # 시간 포맷 통일 (필요한 경우)
        df_logs['timestamp'] = pd.to_datetime(df_logs['timestamp'])
        df_revenue['timestamp'] = pd.to_datetime(df_revenue['timestamp'])


        # 4. 데이터 동기화 및 병합 (Time-based Join/Merge)
        # 로그 데이터를 기준으로 수익화 데이터를 매칭하여 합산
        merged_df = pd.merge_asof(
            df_logs,
            df_revenue,
            on='timestamp',
            direction='nearest',  # 가장 가까운 시간으로 매칭 (근접 동기화)
            tolerance=pd.Timedelta(minutes=5) # 5분 이내의 오차 허용 설정
        )

        if merged_df.empty:
            print("⚠️ 경고: Timestamp 동기화 후 병합된 데이터가 없습니다.")
            return None

        # 5. 핵심 KPI 집계 (예시: 시청 지속률 기반 수익 측정)
        # 예시 KPI: 각 영상 세그먼트별 평균 시청 시간과 해당 시간 동안의 수익 합산
        merged_df['time_spent'] = merged_df['end_time'] - merged_df['start_time'] # start/end time이 있다고 가정
        merged_df['revenue'] = merged_df['monetization_value'].fillna(0) # 수익 데이터가 없는 경우 0으로 채움

        # 최종 집계: 영상 ID 또는 세그먼트별로 그룹화하여 평균 계산
        kpi_results = merged_df.groupby('video_id').agg(
            total_viewing_time=('time_spent', 'sum'),
            total_revenue=('revenue', 'sum'),
            average_watch_duration=('time_spent', 'mean')
        ).reset_index()

        print("✅ KPI 집계 완료.")
        return kpi_results

    except FileNotFoundError as e:
        print(f"❌ 파일 로드 오류: 파일을 찾을 수 없습니다. 경로를 확인해주세요. ({e})")
        return None
    except Exception as e:
        print(f"💥 데이터 처리 중 예상치 못한 오류 발생: {e}")
        return None

if __name__ == "__main__":
    # --- 실제 실행 예시 (실제 파일 경로로 대체 필요) ---
    LOG_FILE = "sessions/2026-05-31T18-37/video_logs.json" # 예시 경로
    REVENUE_FILE = "sessions/2026-06-01T01-52/monetization_data.json" # 예시 경로

    print("\n--- 데이터 파이프라인 테스트 시작 ---")
    # 실제 실행 시, 아래 파일 경로를 정확히 지정해야 합니다.
    result_df = synchronize_and_aggregate_metrics(LOG_FILE, REVENUE_FILE)

    if result_df is not None:
        print("\n--- 최종 KPI 집계 결과 (상위 5개) ---")
        print(result_df.sort_values(by='total_revenue', ascending=False).head())
    else:
        print("\n--- 데이터 파이프라인 실행 실패 ---")