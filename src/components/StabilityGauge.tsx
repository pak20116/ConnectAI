import React from 'react';
import { styled } from '@emotion/styled';

interface StabilityData {
  latencyMs: number;
  visualConsistencyScore: number;
}

interface StabilityGaugeProps {
  data: StabilityData;
  title: string;
  unit: string;
  colorScheme: 'success' | 'warning' | 'danger';
  benchmark: number; // For latency, e.g., 100ms
  maxValue: number; // For VSC, e.g., 100
}

const GaugeContainer = styled.div`
  padding: 20px;
  border-radius: 12px;
  background-color: #f4f7f9;
  margin-bottom: 30px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
`;

const GaugeTitle = styled.h3`
  color: #2C3E50;
  margin-top: 0;
  font-size: 1.4em;
`;

const GaugeValue = styled.div`
  font-size: 2.8em;
  font-weight: 700;
  color: ${props => props.color};
  margin: 10px 0;
`;

const GaugeBar = styled.div`
  height: 30px;
  background-color: #e0e0e0;
  border-radius: 15px;
  overflow: hidden;
  margin-top: 15px;
`;

const GaugeFill = styled.div<{ percentage: number; color: string }>`
  height: 100%;
  width: ${props => `${props.percentage}%`};
  background-color: ${props => props.color};
  transition: width 0.5s ease-in-out;
`;

const StabilityGauge: React.FC<StabilityGaugeProps> = ({ data, title, unit, colorScheme, benchmark, maxValue }) => {
  let statusColor: 'success' | 'warning' | 'danger';
  let percentageValue: number;

  if (title.includes('Latency')) {
    // Latency: Lower is better. Benchmark is 100ms.
    const latencyRatio = data.latencyMs / benchmark;
    if (data.latencyMs <= benchmark * 0.8) {
      statusColor = 'success'; // Very fast
    } else if (data.latencyMs <= benchmark * 1.2) {
      statusColor = 'warning'; // Near benchmark
    } else {
      statusColor = 'danger'; // Slow
    }
    percentageValue = Math.min(100, (data.latencyMs / benchmark) * 100);

  } else if (title.includes('Visual Consistency')) {
    // VSC: Higher is better. Max is 100.
    percentageValue = Math.min(100, data.visualConsistencyScore);
    if (percentageValue >= 90) {
      statusColor = 'success';
    } else if (percentageValue >= 75) {
      statusColor = 'warning';
    } else {
      statusColor = 'danger';
    }
  }

  return (
    <GaugeContainer>
      <GaugeTitle>{title}</GaugeTitle>
      <GaugeValue color={statusColor}>{percentageValue.toFixed(1)} {unit}</GaugeValue>
      <GaugeBar>
        <GaugeFill percentage={percentageValue} color={statusColor} />
      </GaugeBar>
      <p style={{ marginTop: '10px', fontSize: '0.9em', color: '#666' }}>
        Status: {statusColor.charAt(0).toUpperCase() + statusColor.slice(1)}
      </p>
    </GaugeContainer>
  );
};

export default StabilityGauge;