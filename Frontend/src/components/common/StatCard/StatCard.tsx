import "./StatCard.css";

type Props = {
  title: string;

  value: number;

  subtitle: string;

  variant?: "alerts" | "anomalies" | "risk";
};

const StatCard = ({ title, value, subtitle, variant }: Props) => {
  return (
    <div className={`stat-card ${variant}`}>
      <div className="stat-title">{title}</div>
      <div className="stat-value">{value}</div>
      {subtitle && <p className="stat-subtitle">{subtitle}</p>}
    </div>
  );
};

export default StatCard;
