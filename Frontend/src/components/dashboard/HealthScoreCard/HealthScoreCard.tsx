import "./HealthScoreCard.css";

interface Props {
  score?: number;
  status?: string;
}

const HealthScoreCard = ({ score, status }: Props) => {
  const value = score ?? 0;
  const healthStatus = status ?? "UNKNOWN";

  return (
    <div className="health-card">
      <div className="health-header">Health Score</div>
      <div className="health-score">{value}</div>
      <div className={`health-status ${healthStatus.toLowerCase()}`}>
        {healthStatus}
      </div>
    </div>
  );
};

export default HealthScoreCard;
