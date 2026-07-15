import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  ReferenceLine
} from 'recharts';
import type { RiskPrediction } from "../../../types/prediction";

interface Props {
  prediction: RiskPrediction | null;
}

const PredictionForecastChart = ({ prediction }: Props) => {
  if (!prediction || !prediction.analytics) return null;

  const { forecast_data } = prediction.analytics;

  if (!forecast_data || forecast_data.length === 0) {
    return (
      <div className="forecast-chart-container" style={{ width: '100%', height: 350, background: 'rgba(255,255,255,0.02)', padding: '20px', borderRadius: '12px', marginTop: '20px', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
        <h3 style={{ marginBottom: '10px', color: '#fff', fontSize: '1.2rem', fontWeight: 600 }}>Forecasted Risk Timeline</h3>
        <p style={{ color: '#888' }}>Insufficient Data to generate forecast</p>
      </div>
    );
  }

  const currentRisk = prediction.risk_score;
  
  const data = [
    { time: 'Now', risk: currentRisk },
    { time: '+1h', risk: forecast_data[0] },
    { time: '+2h', risk: forecast_data[1] },
    { time: '+3h', risk: forecast_data[2] },
    { time: '+4h', risk: forecast_data[3] },
    { time: '+5h', risk: forecast_data[4] },
    { time: '+6h', risk: forecast_data[5] },
  ];

  return (
    <div className="forecast-chart-container" style={{ width: '100%', height: 350, background: 'rgba(255,255,255,0.02)', padding: '20px', borderRadius: '12px', marginTop: '20px' }}>
      <h3 style={{ marginBottom: '20px', color: '#fff', fontSize: '1.2rem', fontWeight: 600 }}>Forecasted Risk Timeline (Next 6 Hours)</h3>
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="#333" />
          <XAxis dataKey="time" stroke="#aaa" />
          <YAxis domain={[0, 100]} stroke="#aaa" />
          <Tooltip contentStyle={{ backgroundColor: '#1e1e2d', border: '1px solid #333', color: '#fff', borderRadius: '8px' }} />
          <ReferenceLine y={80} label={{ position: 'top', value: 'Critical Risk Threshold', fill: '#ff4d4f' }} stroke="#ff4d4f" strokeDasharray="3 3" />
          <Line 
            type="monotone" 
            dataKey="risk" 
            stroke="#8884d8" 
            strokeWidth={3}
            dot={{ r: 4, fill: '#8884d8', strokeWidth: 2 }} 
            activeDot={{ r: 6, fill: '#fff' }} 
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default PredictionForecastChart;
