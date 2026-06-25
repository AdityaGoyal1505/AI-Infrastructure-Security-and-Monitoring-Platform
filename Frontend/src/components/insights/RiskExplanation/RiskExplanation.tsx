import "./RiskExplanation.css";

interface Props {
  riskScore?: number;

  riskLevel?: string;

  explanation?: string;
}

const RiskExplanation = ({
  riskScore,

  riskLevel,

  explanation,
}: Props) => {
  return (
    <div className="risk-card">
      <div className="risk-header">
        <div>
          <p>Current Risk</p>

          <h2>{riskLevel || "Unknown"}</h2>
        </div>

        <div className="risk-score">{riskScore ?? 0}</div>
      </div>

      <div className="risk-body">
        <h3>AI Explanation</h3>

        <p>{explanation || "No explanation available"}</p>
      </div>
    </div>
  );
};

export default RiskExplanation;
