import StatCard from "../../components/common/StatCard/StatCard";
import AnomalyTable from "../../components/dashboard/AnomalyTable/AnomalyTable";
import HealthScoreCard from "../../components/dashboard/HealthScoreCard/HealthScoreCard";
import RCASection from "../../components/dashboard/RCASection/RCASection";
import RecommendationList from "../../components/dashboard/RecommendationList/RecommendationList";
import { useDashboard } from "../../hooks/useDashboard";
import "./Dashboard.css";

const Dashboard = () => {
  const { data, loading, error } = useDashboard();

  if (loading) {
    return <div className="dashboard-loading">Loading Dashboard...</div>;
  }

  if (error) {
    return <div className="dashboard-error">{error}</div>;
  }

  return (
    <div className="dashboard">
      <div className="stats-grid">
        <HealthScoreCard
          score={data?.health_score?.score}
          status={data?.health_score?.status}
        />
        <StatCard
          variant="alerts"
          title="Active Alerts"
          value={data?.alerts_count ?? 0}
          subtitle="Unresolved"
        />

        <StatCard
          variant="anomalies"
          title="Anomalies"
          value={data?.anomaly_count ?? 0}
          subtitle="Detected"
        />

        <StatCard
          variant="risk"
          title="Risk Score"
          value={data?.risk_prediction?.risk_score ?? 0}
          subtitle={data?.risk_prediction?.risk_level || "Unknown"}
        />
      </div>
      <div className="ai-grid">
        <RCASection
          rootCause={data?.latest_rca?.root_cause}
          summary={data?.latest_rca?.summary}
          confidence={data?.latest_rca?.confidence}
        />
        <RecommendationList recommendations={data?.recommendations ?? []} />
      </div>
      <AnomalyTable anomalies={data?.recent_anomalies ?? []} />
    </div>
  );
};

export default Dashboard;
