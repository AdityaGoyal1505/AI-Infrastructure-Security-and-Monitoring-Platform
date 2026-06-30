import type { RiskPrediction } from "../../../types/prediction";
import "./PredictionCard.css";

interface Props {
  prediction: RiskPrediction | null;
}

const PredictionCard = ({ prediction }: Props) => {
  if (!prediction) {
    return <div className="prediction-card">No prediction available</div>;
  }

  return (
    <div className="prediction-card">
      <div className="prediction-header">
        <h2>AI Risk Analysis</h2>

        <div className={`risk-badge ${prediction.risk_level.toLowerCase()}`}>
          {prediction.risk_level}
        </div>
      </div>

      <div className="prediction-info" style={{ display: 'flex', gap: '2rem', flexWrap: 'wrap' }}>
        <div>
          <span>Node</span>
          <h3>{prediction.node_id}</h3>
        </div>

        <div>
          <span>Risk Score</span>
          <h3>{prediction.risk_score}</h3>
        </div>

        {prediction.analytics && (
          <>
            <div>
              <span>Stability Index</span>
              <h3>{prediction.analytics.stability_index}/100</h3>
            </div>
            <div>
              <span>Incident Probability</span>
              <h3>{prediction.analytics.incident_probability}%</h3>
            </div>
            <div>
              <span>Health Trend</span>
              <h3>{prediction.analytics.health_trend}</h3>
            </div>
            <div>
              <span>Predicted Failure Window</span>
              <h3>{prediction.analytics.estimated_failure_window}</h3>
            </div>
          </>
        )}
      </div>

      <div className="prediction-explanation">
        <h4>Explanation</h4>
        <p>{prediction.explanation}</p>
      </div>
    </div>
  );
};

export default PredictionCard;
