import type { RiskPrediction } from "../../../types/prediction";
import { LineChart, Line, YAxis } from 'recharts';
import "./PredictionHistory.css";

interface Props {
  predictions: RiskPrediction[];
}

const PredictionHistory = ({ predictions }: Props) => {
  // Sort by latest
  const sortedPredictions = [...predictions].sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime());

  return (
    <div className="prediction-history" style={{ marginTop: '30px' }}>
      <h2>Prediction History</h2>

      <table style={{ width: '100%', borderCollapse: 'collapse', marginTop: '20px' }}>
        <thead>
          <tr style={{ borderBottom: '1px solid #333', textAlign: 'left', color: '#aaa' }}>
            <th style={{ padding: '12px' }}>Timestamp</th>
            <th style={{ padding: '12px' }}>Node</th>
            <th style={{ padding: '12px' }}>Risk Badge</th>
            <th style={{ padding: '12px' }}>Trend</th>
            <th style={{ padding: '12px' }}>Forecast Sparkline</th>
            <th style={{ padding: '12px' }}>Confidence</th>
          </tr>
        </thead>

        <tbody>
          {sortedPredictions.map((item) => {
            const date = new Date(item.created_at);
            const trend = item.analytics?.health_trend || "Stable";
            const trendIcon = trend.includes("Degrading") ? "↑" : (trend === "Improving" || trend === "Recovering" ? "↓" : "→");
            const trendColor = trend.includes("Degrading") ? "#ff4d4f" : (trend === "Improving" || trend === "Recovering" ? "#4caf50" : "#aaa");
            
            const forecastData = item.analytics?.forecast_data?.map((val, i) => ({ i, val })) || [];

            return (
              <tr key={item.id} style={{ borderBottom: '1px solid #222' }}>
                <td style={{ padding: '12px', color: '#ccc' }}>
                  {date.toLocaleDateString()} {date.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}
                </td>
                
                <td style={{ padding: '12px', fontWeight: 'bold' }}>{item.node_id}</td>
                
                <td style={{ padding: '12px' }}>
                  <span
                    className={`history-badge ${item.risk_level.toLowerCase()}`}
                    style={{ padding: '4px 8px', borderRadius: '4px', fontSize: '0.8rem' }}
                  >
                    {item.risk_level} ({item.risk_score})
                  </span>
                </td>

                <td style={{ padding: '12px', color: trendColor, fontWeight: 'bold' }}>
                  {trendIcon} {trend}
                </td>

                <td style={{ padding: '12px' }}>
                  {forecastData.length > 0 ? (
                    <LineChart width={80} height={30} data={forecastData}>
                      <YAxis domain={[0, 100]} hide={true} />
                      <Line type="monotone" dataKey="val" stroke={trendColor} strokeWidth={2} dot={false} />
                    </LineChart>
                  ) : (
                    <span style={{ color: '#555', fontSize: '0.8rem' }}>Insufficient Data</span>
                  )}
                </td>

                <td style={{ padding: '12px', color: '#888' }}>
                  {item.analytics?.confidence_score ? `${item.analytics.confidence_score}%` : 'N/A'}
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
};

export default PredictionHistory;
