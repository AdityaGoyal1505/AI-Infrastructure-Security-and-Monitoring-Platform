import "./PredictionStats.css";

interface Props {
  highestRisk: number;

  highRiskNodes: number;

  riskLevel: string;
}

const PredictionStats = ({
  highestRisk,

  highRiskNodes,

  riskLevel,
}: Props) => {
  return (
    <div className="prediction-stats">
      <div className="prediction-stat-card risk">
        <p>Highest Risk</p>

        <h2>{highestRisk}</h2>
      </div>

      <div className="prediction-stat-card nodes">
        <p>Nodes At Risk</p>

        <h2>{highRiskNodes}</h2>
      </div>

      <div className="prediction-stat-card level">
        <p>Risk Level</p>

        <h2>{riskLevel}</h2>
      </div>
    </div>
  );
};

export default PredictionStats;
