import type { RiskPrediction } from "../../../types/prediction";

import "./PredictionHistory.css";

interface Props {
  predictions: RiskPrediction[];
}

const PredictionHistory = ({ predictions }: Props) => {
  return (
    <div className="prediction-history">
      <h2>Prediction History</h2>

      <table>
        <thead>
          <tr>
            <th>Node</th>

            <th>Risk</th>

            <th>Score</th>

            <th>Date</th>
          </tr>
        </thead>

        <tbody>
          {predictions.map((item) => (
            <tr key={item.id}>
              <td>{item.node_id}</td>

              <td>
                <span
                  className={`history-badge

${item.risk_level.toLowerCase()}

`}
                >
                  {item.risk_level}
                </span>
              </td>

              <td>{item.risk_score}</td>

              <td>{new Date(item.created_at).toLocaleDateString()}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default PredictionHistory;
