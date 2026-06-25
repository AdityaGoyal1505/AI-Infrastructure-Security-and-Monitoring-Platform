import "./Trends.css";

import useTrends from "../../hooks/useTrends";

import TopInsightCard from "../../components/trends/TopInsightCard/TopInsightCard";

import OccurrenceChart from "../../components/trends/OccurrenceChart/OccurrenceChart";

import TrendList from "../../components/trends/TrendList/TrendList";

import TrendSummary from "../../components/trends/TrendSummary/TrendSummary";

const Trends = () => {
  const {
    data,

    loading,

    error,

    topInsight,
  } = useTrends();

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

      <TopInsightCard insight={topInsight} />

      <OccurrenceChart trends={data} />

      <TrendList trends={data} />

      <TrendSummary topInsight={topInsight} />
    </div>
  );
};

export default Trends;
