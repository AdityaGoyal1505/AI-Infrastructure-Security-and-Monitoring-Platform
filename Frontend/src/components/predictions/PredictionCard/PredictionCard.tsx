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

        <div
          className={`risk-badge

${prediction.risk_level.toLowerCase()}

`}
        >
          {prediction.risk_level}
        </div>
      </div>

      <div className="prediction-info">
        <div>
          <span>Node</span>

          <h3>{prediction.node_id}</h3>
        </div>

        <div>
          <span>Risk Score</span>

          <h3>{prediction.risk_score}</h3>
        </div>
      </div>

      <div className="prediction-explanation">
        <h4>Explanation</h4>

        <p>{prediction.explanation}</p>
      </div>
    </div>
  );
};

export default PredictionCard;
