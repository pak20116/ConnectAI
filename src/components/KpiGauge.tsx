import React from 'react';

// KPI 데이터 구조 정의 (Designer에게 전달할 최종 포맷)
interface KpiData {
  label: string;
  value: number;
  target: number;
  unit: string;
  color: 'success' | 'warning' | 'danger'; // 시각화에 사용할 색상 상태
}

// 게이지 컴포넌트 타입 정의
interface KpiGaugeProps {
  data: KpiData;
}

/**
 * KPI 게이지 컴포넌트: 시스템 안정성 지표 시각화
 * Latency_ms 또는 VisualConsistencyScore를 시각적으로 표현합니다.
 */
const KpiGauge: React.FC<KpiGaugeProps> = ({ data }) => {
  // 게이지 채움 비율 계산 (0에서 100 사이)
  const percentage = Math.min(100, (data.value / data.target) * 100);

  // 색상 결정 로직: 목표치 대비 현재 값의 상태에 따라 결정
  let gaugeColor: 'success' | 'warning' | 'danger';

  if (data.value >= data.target) {
    gaugeColor = 'success'; // 목표 달성 시 성공색
  } else if (data.value >= data.target * 0.9) {
    gaugeColor = 'warning'; // 목표에 근접 시 경고색
  } else {
    gaugeColor = 'danger'; // 목표 미달 시 위험색
  }

  const gaugeStyle: React.CSSProperties = {
    width: '100%',
    height: '200px',
    borderRadius: '10px',
    backgroundColor: '#e0e0e0',
    overflow: 'hidden',
    border: '1px solid #ccc',
    position: 'relative',
  };

  const fillStyle: React.CSSProperties = {
    height: '100%',
    width: `${percentage}%`,
    backgroundColor: gaugeColor === 'success' ? '#4CAF50' : gaugeColor === 'warning' ? '#FFC107' : '#F44336',
    transition: 'width 0.5s ease-in-out',
  };

  return (
    <div style={{ marginBottom: '20px' }}>
      <div style={{ fontSize: '1.2em', fontWeight: 'bold', marginBottom: '10px' }}>
        {data.label}
      </div>
      <div style={gaugeStyle}>
        <div style={fillStyle}></div>
      </div>
      <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: '5px', fontSize: '0.9em' }}>
        <span>{data.value.toFixed(2)}</span>
        <span>{data.target}</span>
        <span>{data.unit}</span>
      </div>
    </div>
  );
};

export default KpiGauge;