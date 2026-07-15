import "./ExecutiveSummary.css";

interface ExecutiveMetrics {
  overall_trend: string;
  avg_health_score: number | null;
  active_anomalies: number;
  risk_trend: string;
  stability: string;
  explanation: string;
}

interface Props {
  metrics: ExecutiveMetrics | null;
}

const ExecutiveSummary = ({ metrics }: Props) => {
  if (!metrics) {
    return null;
  }

  return (
    <div className="executive-summary-card">
      <div className="executive-header">
        <h2>AI Executive Summary</h2>
        <p>Infrastructure behavior and predictive analysis</p>
      </div>

      <div className="metrics-grid">
        <div className="metric-tile">
          <span className="metric-label">Overall Trend</span>
          <span className="metric-value">{metrics.overall_trend}</span>
        </div>
        <div className="metric-tile">
          <span className="metric-label">Avg Health Score</span>
          <span className="metric-value">
            {metrics.avg_health_score !== null ? metrics.avg_health_score : "N/A"}
          </span>
        </div>
        <div className="metric-tile">
          <span className="metric-label">Active Anomalies</span>
          <span className="metric-value">{metrics.active_anomalies}</span>
        </div>
        <div className="metric-tile">
          <span className="metric-label">Risk Trend</span>
          <span className="metric-value">{metrics.risk_trend}</span>
        </div>
        <div className="metric-tile">
          <span className="metric-label">Stability</span>
          <span className="metric-value">{metrics.stability}</span>
        </div>
      </div>

      <div className="ai-explanation">
        <span className="ai-icon">✨</span>
        <p>{metrics.explanation}</p>
      </div>
    </div>
  );
};

export default ExecutiveSummary;
