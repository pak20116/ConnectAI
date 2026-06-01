# 자동화된 썸네일 생성 파이프라인: 최종 품질 게이트 및 배포 가이드라인

## 1. 품질 게이트 정의 (Quality Gate Definition)

자동화 파이프라인의 실행에 앞서 반드시 통과해야 하는 조건(Gate)을 정의합니다. 이 게이트는 데이터 안정성 지표와 시각적 일관성을 결합하여 구성됩니다.

| 게이트 항목 | 측정 기준 (Source) | 요구 조건 (Requirement) | 관련 에이전트 |
| :--- | :--- | :--- | :--- |
| **데이터 안정성** | Process Success Rate (PSR) | $\text{PSR} \ge 98\%$ (오류율 $\text{ER} \le 2\%$) | 코다리 |
| **데이터 무결성** | Error Rate (ER) | 모든 데이터 필드(Source, Process, Output)의 일치성 검증 통과 ($\text{ER}=0$) | 코다리/현빈 |
| **시각적 일관성** | Visual Consistency Check | 썸네일 디자인이 VCVM 가이드라인 내에서 $\pm 5\%$ 이내로 구현되었는지 확인 (색상, 타이포그래피) | Designer |
| **브랜드 준수** | Brand Compliance | 필수 색상 팔레트 ($\#2C3E50$ 계열) 및 로고 배치 규칙 엄격 준수 | Designer |

## 2. 디자인 가이드라인 통합 (Visual System Integration)

모든 자동 생성 결과물이 Cortexa의 브랜드 정체성을 반영하도록 시각적 규칙을 명시합니다.

**A. 컬러 시스템 (Color System)**
*   **Primary Color:** `#2C3E50` (기술적이고 전문적인 느낌 강조)
*   **Secondary Accent:** `#1ABC9C` (포인트 및 강조에 사용)
*   **Background/Neutral:** `#ECF0F1` (여백과 가독성 확보)

**B. 타이포그래피 시스템 (Typography System)**
*   **Headline Font:** Montserrat Bold (강조 메시지용)
*   **Body Font:** Open Sans (정보 전달용)
*   **Rule:** 모든 텍스트는 대비를 극대화하여 가독성을 확보해야 하며, 헤드라인은 Primary Color 또는 Accent Color로 강조되어야 합니다.

**C. 레이아웃 및 구성 원칙 (Layout & Composition)**
1.  **Focus/Escape Zone 명확화:** 썸네일 내에서 시청자의 시선이 가장 먼저 머무는 영역(Focus)과 다음으로 이동할 영역(Escape)을 명확히 구분하는 시각적 분할선을 적용합니다. (이는 레오의 'Focus & Escape' 전략 반영)
2.  **로고 배치:** 로고는 우측 상단 또는 좌측 하단에 일관된 크기와 여백(Padding)을 유지하며, 배경 색상과 명확히 대비되어야 합니다.
3.  **정보 계층 구조:** 핵심 메시지($\text{Focus}$) $\rightarrow$ 보조 정보 ($\text{Escape}$) $\rightarrow$ 브랜드 요소(로고/색상)의 순서로 시각적 계층을 설정합니다.

## 3. 배포 가이드라인 (Deployment Guideline)

자동화된 파이프라인 실행 및 결과물 배포를 위한 최종 절차입니다.

**단계 1: 데이터 입력 및 검증 (Input & Validation)**
*   **입력:** 콘텐츠 스크립트 및 목표 KPI 설정 파일 로드.
*   **검증:** `pipeline_executor.py`가 $\text{PSR} \ge 98\%$ 조건을 만족하는지 확인. 실패 시, 데이터 오류 보고서를 즉시 생성하고 파이프라인을 중단(Halt).

**단계 2: 비주얼 생성 (Visual Generation)**
*   검증 통과 시, Designer의 **'브랜드 비주얼 자산 라이브러리'**에서 적절한 레이아웃 템플릿을 선택하여 적용.
*   선택된 템플릿은 반드시 정의된 Primary Color 및 타이포그래피 규칙을 준수해야 함.

**단계 3: 품질 게이트 통과 (Final Quality Gate Check)**
*   생성된 썸네일이 **'시각적 일관성 검사'**를 통과하는지 자동화된 픽셀 분석 모듈(Designer의 도구 활용)을 통해 확인.
    *   *실패 조건:* 색상 편차 $\pm 5\%$ 초과, 필수 요소 위치 이탈 발생 시, **"Visual Inconsistency Detected: [오류 상세 내용]"** 로그를 기록하고 결과물을 보류.

**단계 4: 배포 (Deployment)**
*   품질 게이트 통과 시, 최종 썸네일을 지정된 저장소에 배포 및 KPI 대시보드에 결과 연결.
*   실패 시, 오류 보고서를 기반으로 수동 검토(Manual Review)를 요청하고 재실행을 위한 피드백 루프를 시작.