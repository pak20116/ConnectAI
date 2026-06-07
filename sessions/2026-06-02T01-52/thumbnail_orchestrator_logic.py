# thumbnail_orchestrator_logic.py
import time
from typing import Dict, Any

# VCVM 규칙 정의 (Designer가 제공한 프레임워크 기반)
VCVM_RULES = {
    "consistency_threshold": 0.95,  # 최소 일관성 점수
    "latency_limit_ms": 5000,     # 최대 허용 지연 시간 (5초)
    "chaos_factor_weight": 0.6,   # 혼돈 요소의 가중치
    "control_factor_weight": 0.4  # 통제 요소의 가중치
}

def calculate_visual_consistency(chaos_data: Dict[str, Any], control_data: Dict[str, Any]) -> float:
    """
    VCVM 규칙에 따라 시각적 일관성 점수를 계산합니다.
    Chaos와 Control 데이터 간의 대비를 측정합니다.
    """
    # 예시 로직: 두 요소 간의 차이를 기반으로 점수 계산 (실제 구현은 프롬프트/이미지 분석 결과에 따라 조정 필요)
    chaos_score = chaos_data.get("visual_entropy", 0.5)  # 혼돈 데이터로부터 엔트로피 측정
    control_score = control_data.get("structure_adherence", 0.5) # 통제 데이터로부터 구조 준수 측정

    # VCVM 규칙을 반영하여 최종 점수 계산
    consistency = (chaos_score * VCVM_RULES["chaos_factor_weight"]) + \
                  (control_score * VCVM_RULES["control_factor_weight"])

    # 0.0에서 1.0 사이로 정규화 및 제한
    final_score = min(1.0, max(0.0, consistency))
    return final_score

def measure_latency(start_time: float, end_time: float) -> float:
    """
    프로세스 실행에 걸린 지연 시간(Latency)을 밀리초 단위로 측정합니다.
    """
    elapsed = end_time - start_time
    return elapsed * 1000  # 밀리초 반환

def run_thumbnail_orchestrator(input_prompt: str, system_config: Dict[str, Any]) -> Dict[str, Any]:
    """
    썸네일 자동화 프로세스를 시뮬레이션하고 KPI를 측정합니다.
    실제 API 호출 대신 시뮬레이션을 위해 임의의 지연 시간을 추가합니다.
    """
    start_time = time.time()

    # 1. Chaos/Control 데이터 생성 (시뮬레이션)
    chaos_data = {"visual_entropy": 0.75}  # 예시 값
    control_data = {"structure_adherence": 0.88} # 예시 값

    # 2. 핵심 로직 실행 (실제로는 이미지 생성 및 분석이 들어감)
    consistency_score = calculate_visual_consistency(chaos_data, control_data)

    # 3. Latency 측정 시뮬레이션
    time.sleep(0.5) # 실제 작업 시간 시뮬레이션
    end_time = time.time()
    latency_ms = measure_latency(start_time, end_time)

    result = {
        "consistency_score": round(consistency_score, 4),
        "latency_ms": round(latency_ms, 2),
        "raw_chaos": chaos_data,
        "raw_control": control_data
    }

    return result

if __name__ == "__main__":
    # 테스트 실행 예시
    mock_prompt = "A complex flow of data visualization."
    mock_config = {"model_version": "v1.2"}

    print(f"--- 썸네일 자동화 시뮬레이션 시작 ---")
    metrics = run_thumbnail_orchestrator(mock_prompt, mock_config)
    print("\n✅ 계산된 KPI 결과:")
    print(f"VisualConsistencyScore: {metrics['consistency_score']}")
    print(f"Latency_ms: {metrics['latency_ms']}")

    # VCVM 규칙 검증 (Self-Check)
    if metrics['consistency_score'] >= VCVM_RULES["consistency_threshold"] and \
       metrics['latency_ms'] <= VCVM_RULES["latency_limit_ms"]:
        print("\n✅ 최종 시스템 검증 통과: 모든 KPI 기준을 만족합니다.")
    else:
        print("\n❌ 최종 시스템 검증 실패: KPI 중 하나 이상 기준에 미달했습니다.")

<create_file path="sessions/2026-06-02T01-52/test_thumbnail_orchestrator.py">
# test_thumbnail_orchestrator.py
import unittest
from thumbnail_orchestrator_logic import (
    calculate_visual_consistency,
    measure_latency,
    run_thumbnail_orchestrator,
    VCVM_RULES
)

class TestThumbnailOrchestrator(unittest.TestCase):
    """썸네일 자동화 로직의 KPI 계산 정확성을 검증합니다."""

    def test_consistency_calculation_high_match(self):
        """높은 일관성 조건에서 점수가 올바르게 계산되는지 확인합니다."""
        chaos = {"visual_entropy": 1.0}  # 최대 혼돈
        control = {"structure_adherence": 1.0} # 최대 통제
        
        # 기대값 계산 (가중치 적용)
        expected_score = (1.0 * VCVM_RULES["chaos_factor_weight"]) + \
                         (1.0 * VCVM_RULES["control_factor_weight"])
        
        calculated_score = calculate_visual_consistency(chaos, control)
        self.assertAlmostEqual(calculated_score, expected_score, places=4, msg="최대 일치 시 일관성 점수 계산 오류")

    def test_consistency_calculation_low_match(self):
        """낮은 일관성 조건에서 점수가 올바르게 계산되는지 확인합니다."""
        chaos = {"visual_entropy": 0.1}  # 낮은 혼돈
        control = {"structure_adherence": 0.1} # 낮은 통제
        
        expected_score = (0.1 * VCVM_RULES["chaos_factor_weight"]) + \
                         (0.1 * VCVM_RULES["control_factor_weight"])
        
        calculated_score = calculate_visual_consistency(chaos, control)
        self.assertAlmostEqual(calculated_score, expected_score, places=4, msg="최소 일치 시 일관성 점수 계산 오류")

    def test_latency_measurement(self):
        """지연 시간 측정 로직이 정확하게 밀리초를 반환하는지 확인합니다."""
        start = time.time()
        # 약간의 지연을 인위적으로 추가하여 측정값을 보장
        time.sleep(0.05) 
        end = time.time()
        
        actual_latency = measure_latency(start, end)
        self.assertTrue(actual_latency > 0, "지연 시간은 양수여야 합니다.")
        # 실제 측정값에 대한 엄격한 비교는 환경에 따라 달라질 수 있으므로 범위 확인으로 대체
        self.assertLess(actual_latency, 5000, "측정된 지연 시간이 허용치(5초)를 초과했습니다.")

    def test_orchestrator_integration(self):
        """전체 실행 흐름이 KPI 측정에 성공적으로 통합되었는지 확인합니다."""
        # 이 테스트는 실제 외부 API 호출 없이 내부 로직의 흐름 검증에 중점을 둡니다.
        result = run_thumbnail_orchestrator("Test Prompt", {"model_version": "v1"})
        
        self.assertIn("consistency_score", result)
        self.assertIn("latency_ms", result)
        
        # 성공적인 시뮬레이션 결과가 도출되었는지 확인 (실제 값보다는 구조 확인)
        self.assertTrue(isinstance(result['consistency_score'], float))

if __name__ == '__main__':
    unittest.main()