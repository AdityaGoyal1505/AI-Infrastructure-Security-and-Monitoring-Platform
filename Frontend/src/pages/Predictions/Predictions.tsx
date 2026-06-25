import "./Predictions.css";

import usePredictions from "../../hooks/usePredictions";

import PredictionStats from "../../components/predictions/PredictionStats/PredictionStats";

import PredictionCard from "../../components/predictions/PredictionCard/PredictionCard";

import PredictionHistory from "../../components/predictions/PredictionHistory/PredictionHistory";

const Predictions = () => {
  const {
    data,

    loading,

    error,

    highestRisk,

    highRiskNodes,
  } = usePredictions();

  if (loading) {
    return <div className="predictions-loading">Loading Predictions...</div>;
  }

  if (error) {
    return <div className="predictions-error">{error}</div>;
  }

  return (
    <div className="predictions-page">
      <div className="predictions-header">
        <h1>AI Predictions</h1>

        <p>Predict infrastructure risks before they become incidents.</p>
      </div>

      <PredictionStats
        highestRisk={highestRisk ? Math.round(highestRisk.risk_score) : 0}
        highRiskNodes={highRiskNodes.length}
        riskLevel={highestRisk ? highestRisk.risk_level : "UNKNOWN"}
      />

      <PredictionCard prediction={highestRisk} />

      <PredictionHistory predictions={data} />
    </div>
  );
};

export default Predictions;
