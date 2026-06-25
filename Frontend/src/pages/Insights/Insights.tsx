import "./Insights.css";

import { useDashboard } from "../../hooks/useDashboard";

import InsightList from "../../components/insights/InsightList/InsightList";

import RiskExplanation from "../../components/insights/RiskExplanation/RiskExplanation.tsx";

import AIChatPanel from "../../components/insights/AIChatPanel/AIChatPanel";

const Insights = () => {
  const {
    data,

    loading,

    error,
  } = useDashboard();

  if (loading) {
    return <div className="insight-loading">Loading...</div>;
  }

  if (error) {
    return <div className="insight-loading">{error}</div>;
  }

  return (
    <div className="insights-page">
      <InsightList insights={data?.top_insights ?? []} />

      <RiskExplanation
        riskScore={data?.risk_prediction?.risk_score}
        riskLevel={data?.risk_prediction?.risk_level}
        explanation={data?.risk_prediction?.explanation}
      />

      <AIChatPanel />
    </div>
  );
};

export default Insights;
