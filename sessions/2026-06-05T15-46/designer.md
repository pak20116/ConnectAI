# Sales Page UI/UX Design Guide: Stability Proof Section
## 🎨 디자인 목표
시스템 안정성 KPI(Latency_ms, VisualConsistencyScore)를 시각적으로 증명하여 프리미엄 가치를 정당화하는 다크 모드 기반의 기술적 신뢰성 강조 레이아웃을 설계한다.

## 📐 핵심 디자인 원칙
- **톤:** 기술적, 전문적, 안정적 (Technical, Professional, Stable).
- **Primary Color:** #2C3E50 (신뢰감)
- **Accent Color:** #1ABC9C (안정성/성공 강조)
- **Background:** #1F2833 (어두운 배경)

## 📊 KPI 시각화 컴포넌트 상세 설계

### A. Latency_ms Gauge (실시간 성능 게이지)
- **컴포넌트:** Circular Gauge + Digital Readout.
- **레이아웃:** 중앙에 배치하여 실시간 성능 통제를 강조.
- **디자인:** 배경은 #34495E. 채워지는 부분은 Accent Color(#1ABC9C). 목표값(Target: 100ms)과 현재 값(X ms)을 명확히 표시하고, 상태에 따라 색상 변화 (Optimal=Green, Warning=Yellow).

### B. Visual Consistency Score Progress Bar (시각적 일관성 바)
- **컴포넌트:** Horizontal Progress Bar.
- **레이아웃:** Latency Gauge 아래에 배치하여 품질 보장을 연결.
- **디자인:** 전체 길이를 100%로 설정하고, 진행률을 Accent Color(#1ABC9C)로 표시. 결과 값(X / 100)과 함께 "Consistency Score X%" 메시지를 명시.

## 📝 최종 레이아웃 시각화 (Conceptual Mockup Structure)
- **Hero:** 강력한 헤드라인 및 핵심 가치 제시.
- **Stability Proof Section:** Latency Gauge와 Consistency Progress Bar를 배치하여 기술적 안정성을 즉각적으로 증명.
- **Features:** 제공되는 Deliverables를 아이콘과 함께 정리.
- **Pricing & CTA:** 명확한 가격 책정 및 강력한 행동 유도 버튼.