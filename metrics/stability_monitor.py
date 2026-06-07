import time
import json
from typing import Dict, Any

# 시스템 안정성 지표 측정 프레임워크
class StabilityMonitor:
    """
    시스템의 Latency 및 시각적 일관성(Visual Consistency)을 측정하고 모니터링하는 클래스.
    """
    def __init__(self, target_latency_ms: float = 100.0, consistency_threshold: float = 0.95):
        """
        초기화 메서드. 목표 Latency와 일관성 임계값을 설정합니다.
        :param target_latency_ms: 목표 지연 시간 (밀리초).
        :param consistency_threshold: 시각적 일관성의 최소 허용치 (0.0 ~ 1.0).
        """
        self.target_latency_ms = target_latency_ms
        self.consistency_threshold = consistency_threshold
        self.metrics: Dict[str, Any] = {
            "latency_history": [],
            "consistency_score": [],
            "timestamp": time.time()
        }

    def record_latency(self, actual_latency_ms: float) -> None:
        """
        실제 측정된 지연 시간을 기록합니다.
        """
        self.metrics["latency_history"].append({
            "time": time.time(),
            "latency_ms": actual_latency_ms
        })

    def record_consistency(self, score: float) -> None:
        """
        시각적 일관성 점수를 기록합니다.
        """
        self.metrics["consistency_score"].append({
            "time": time.time(),
            "score": score
        })

    def calculate_stability(self) -> Dict[str, Any]:
        """
        현재까지의 데이터를 기반으로 시스템 안정성을 계산합니다.
        """
        if not self.metrics["latency_history"] and not self.metrics["consistency_score"]:
            return {"status": "No Data", "message": "측정된 데이터가 없습니다."}

        # Latency 분석: 평균 및 최대값 계산
        latencies = [m['latency_ms'] for m in self.metrics["latency_history"]]
        if latencies:
            avg_latency = sum(latencies) / len(latencies)
            max_latency = max(latencies)
            latency_status = "OK" if avg_latency <= self.target_latency_ms else "WARNING"
        else:
            avg_latency, max_latency, latency_status = 0.0, 0.0, "N/A"

        # Consistency 분석: 평균 점수 계산
        consistency_scores = [m['score'] for m in self.metrics["consistency_score"]]
        if consistency_scores:
            avg_consistency = sum(consistency_scores) / len(consistency_scores)
            consistency_status = "OK" if avg_consistency >= self.consistency_threshold else "WARNING"
        else:
            avg_consistency, consistency_status = 0.0, "N/A"


        result = {
            "timestamp": self.metrics["timestamp"],
            "latency_analysis": {
                "average_latency_ms": round(avg_latency, 2),
                "max_latency_ms": round(max_latency, 2),
                "status": latency_status,
                "target_ms": self.target_latency_ms
            },
            "consistency_analysis": {
                "average_consistency_score": round(avg_consistency, 4),
                "status": consistency_status,
                "threshold": self.consistency_threshold
            },
            "overall_stability": "OK" if latency_status == "OK" and consistency_status == "OK" else "WARNING"
        }
        return result

def monitor_system(start_latency: float = 100.0, consistency: float = 0.95) -> StabilityMonitor:
    """
    시스템 모니터링을 시작하는 메인 함수입니다.
    """
    monitor = StabilityMonitor(target_latency_ms=start_latency, consistency_threshold=consistency)
    print(f"🚀 시스템 안정성 모니터링 프레임워크를 초기화했습니다. 목표 Latency: {start_latency}ms, 일관성 임계값: {consistency}")
    return monitor

if __name__ == "__main__":
    # 테스트 시뮬레이션 시작
    monitor = monitor_system(start_latency=100.0, consistency=0.95)

    print("\n--- 시뮬레이션 데이터 기록 시작 ---")

    # 1. Latency 데이터 시뮬레이션 (경우에 따라 지연 시간 변동)
    for i in range(3):
        # 목표치 근처의 랜덤 레이턴시 시뮬레이션
        simulated_latency = 90 + (i * 5) + (time.time() % 10) # 약간의 변동성 추가
        monitor.record_latency(simulated_latency)
        print(f"Latency 기록: {simulated_latency:.2f}ms")
        time.sleep(0.1)

    # 2. Consistency 데이터 시뮬레이션 (일관성 점수 변동)
    for i in range(3):
        # 목표치 근처의 일관성 점수 시뮬레이션
        simulated_consistency = 0.95 + (i * 0.01) - 0.005 # 약간의 노이즈 추가
        monitor.record_consistency(min(1.0, max(0.0, simulated_consistency)))
        print(f"Consistency 기록: {simulated_consistency:.4f}")
        time.sleep(0.1)

    # 3. 최종 안정성 계산 및 보고
    final_report = monitor.calculate_stability()
    print("\n======================================")
    print("✨ 시스템 안정성 최종 보고서 ✨")
    print("======================================")
    print(json.dumps(final_report, indent=4, ensure_ascii=False))