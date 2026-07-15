import "./Trends.css";
import useTrends from "../../hooks/useTrends";
import ExecutiveSummary from "../../components/trends/ExecutiveSummary/ExecutiveSummary";
import PatternDistributionChart from "../../components/trends/PatternDistributionChart/PatternDistributionChart";
import TrendAnalyticsChart from "../../components/trends/TrendAnalyticsChart/TrendAnalyticsChart";
import InfrastructureEventTimeline from "../../components/trends/InfrastructureEventTimeline/InfrastructureEventTimeline";

const Trends = () => {
  const { loading, error, executiveMetrics, singleNode, charts, timeline } = useTrends();

  if (loading) {
    return <div className="trends-loading">Loading Trends...</div>;
  }

  if (error) {
    return <div className="trends-error">{error}</div>;
  }

  return (
    <div className="trends-page">
      <div className="trends-header">
        <h1>AI Trends</h1>
        <p>
          Discover recurring patterns, monitor infrastructure behavior, and
          uncover hidden insights.
        </p>
      </div>

      <ExecutiveSummary metrics={executiveMetrics} />

      {charts && (
        singleNode ? (
          <TrendAnalyticsChart chartType="health" data={charts.health_score || []} />
        ) : (
          <TrendAnalyticsChart chartType="nodes" data={charts.top_affected_nodes || charts.anomalies || []} />
        )
      )}

      {charts && charts.pattern_distribution && (
        <PatternDistributionChart distribution={charts.pattern_distribution} />
      )}

      <InfrastructureEventTimeline events={timeline || []} />

    </div>
  );
};

export default Trends;
