import time
from typing import Dict, Any, List

# --- Configuration and Constants ---
LATENCY_THRESHOLD_MS = 100  # Latency 병목 지점 검증을 위한 임계값 (밀리초)
VISUAL_CONSISTENCY_TARGET = 0.95  # 시각적 일관성 목표치 (0.0 ~ 1.0)

class StabilityMonitor:
    """
    시스템의 안정성 KPI(Latency, Visual Consistency)를 측정하고 모니터링하는 클래스.
    """
    def __init__(self, system_name: str):
        """
        모니터링 객체를 초기화합니다.
        :param system_name: 모니터링 대상 시스템의 이름 (예: 'VideoPipeline')
        """
        self.system_name = system_name
        self.metrics: Dict[str, Any] = {
            "latency_ms": 0.0,  # 지연 시간 측정 (Latency)
            "visual_consistency_score": 1.0,  # 시각적 일관성 점수
            "timestamp": time.time(),
            "status": "OK"
        }
        print(f"StabilityMonitor initialized for system: {self.system_name}")

    def measure_latency(self, duration_ms: float) -> None:
        """
        특정 작업의 지연 시간을 측정하고 기록합니다.
        :param duration_ms: 측정된 시간 (밀리초).
        """
        self.metrics["latency_ms"] = duration_ms
        if duration_ms > LATENCY_THRESHOLD_MS:
            self.metrics["status"] = "WARNING"
        else:
            self.metrics["status"] = "OK"
        print(f"[{self.system_name}] Latency measured: {duration_ms:.2f} ms. Status: {self.metrics['status']}")

    def measure_visual_consistency(self, score: float) -> None:
        """
        시각적 일관성 점수를 측정하고 기록합니다.
        :param score: 계산된 시각적 일관성 점수 (0.0 ~ 1.0).
        """
        self.metrics["visual_consistency_score"] = max(0.0, min(1.0, score)) # 값 클리핑 방지
        if self.metrics["visual_consistency_score"] < VISUAL_CONSISTENCY_TARGET:
            self.metrics["status"] = "WARNING"
        else:
            self.metrics["status"] = "OK"
        print(f"[{self.system_name}] Visual Consistency measured: {self.metrics['visual_consistency_score']:.4f}. Status: {self.metrics['status']}")

    def get_report(self) -> Dict[str, Any]:
        """
        현재 측정된 모든 안정성 지표를 보고서 형태로 반환합니다.
        """
        return self.metrics

# --- Example Usage (Self-Test Stub) ---
if __name__ == "__main__":
    print("--- Stability Monitor Initializing Test ---")
    monitor = StabilityMonitor("ThumbnailAutomationPipeline")
    
    # 1. Latency 측정 테스트
    print("\n--- Testing Latency Measurement ---")
    # 정상 범위 내의 지연 시간 시뮬레이션
    monitor.measure_latency(50.5)
    # 임계값을 초과하는 지연 시간 시뮬레이션 (경고 발생 예상)
    monitor.measure_latency(150.2)

    # 2. Visual Consistency 측정 테스트
    print("\n--- Testing Visual Consistency Measurement ---")
    # 목표치 미달 점수 시뮬레이션 (경고 발생 예상)
    monitor.measure_visual_consistency(0.90)
    # 목표치 충족 점수 시뮬레이션
    monitor.measure_visual_consistency(0.98)

    print("\n--- Final Report ---")
    final_report = monitor.get_report()
    import json
    print(json.dumps(final_report, indent=4))