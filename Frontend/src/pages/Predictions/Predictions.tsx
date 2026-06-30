import "./Predictions.css";
import usePredictions from "../../hooks/usePredictions";
import PredictionStats from "../../components/predictions/PredictionStats/PredictionStats";
import PredictionHistory from "../../components/predictions/PredictionHistory/PredictionHistory";
import PredictionForecastChart from "../../components/predictions/PredictionForecastChart/PredictionForecastChart";

const Predictions = () => {
  const { data, loading, error, highestRisk, highRiskNodes } = usePredictions();

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

      {highestRisk && highestRisk.analytics && (
        <div className="predictions-metrics-grid" style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '20px', marginTop: '20px' }}>
          
          <div className="metric-card" style={{ background: 'rgba(255,255,255,0.05)', padding: '20px', borderRadius: '12px' }}>
            <span style={{ color: '#aaa', fontSize: '0.9rem' }}>Node</span>
            <h3 style={{ margin: '10px 0 0', fontSize: '1.5rem', color: '#fff' }}>{highestRisk.node_id}</h3>
          </div>

          <div className="metric-card" style={{ background: 'rgba(255,255,255,0.05)', padding: '20px', borderRadius: '12px' }}>
            <span style={{ color: '#aaa', fontSize: '0.9rem' }}>Current Risk</span>
            <h3 style={{ margin: '10px 0 0', fontSize: '1.5rem', color: '#fff' }}>{highestRisk.risk_score}</h3>
            <span style={{ fontSize: '0.8rem', color: highestRisk.analytics.health_trend === 'Improving' ? '#4caf50' : '#ff4d4f' }}>
              {highestRisk.analytics.health_trend === 'Improving' ? '↓ Decreasing' : (highestRisk.analytics.health_trend.includes('Degrading') ? '↑ Increasing' : 'Stable')}
            </span>
          </div>

          <div className="metric-card" style={{ background: 'rgba(255,255,255,0.05)', padding: '20px', borderRadius: '12px' }}>
            <span style={{ color: '#aaa', fontSize: '0.9rem' }}>Health Trend</span>
            <h3 style={{ margin: '10px 0 0', fontSize: '1.5rem', color: '#fff' }}>{highestRisk.analytics.health_trend}</h3>
          </div>

          <div className="metric-card" style={{ background: 'rgba(255,255,255,0.05)', padding: '20px', borderRadius: '12px' }}>
            <span style={{ color: '#aaa', fontSize: '0.9rem' }}>Stability Index</span>
            <h3 style={{ margin: '10px 0 0', fontSize: '1.5rem', color: '#fff' }}>{highestRisk.analytics.stability_index}</h3>
          </div>

          <div className="metric-card" style={{ background: 'rgba(255,255,255,0.05)', padding: '20px', borderRadius: '12px' }}>
            <span style={{ color: '#aaa', fontSize: '0.9rem' }}>Predicted Failure Window</span>
            <h3 style={{ margin: '10px 0 0', fontSize: '1.5rem', color: '#fff' }}>{highestRisk.analytics.estimated_failure_window}</h3>
          </div>

          <div className="metric-card" style={{ background: 'rgba(255,255,255,0.05)', padding: '20px', borderRadius: '12px' }}>
            <span style={{ color: '#aaa', fontSize: '0.9rem' }}>Incident Probability</span>
            <h3 style={{ margin: '10px 0 0', fontSize: '1.5rem', color: '#fff' }}>{highestRisk.analytics.incident_probability}</h3>
          </div>

        </div>
      )}

      {highestRisk && highestRisk.analytics && (
        <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: '20px', marginTop: '20px' }}>
          <div className="ai-explanation-card" style={{ background: 'rgba(255,255,255,0.02)', padding: '20px', borderRadius: '12px' }}>
            <h3 style={{ color: '#fff', marginBottom: '15px' }}>AI Explanation</h3>
            <p style={{ color: '#ddd', lineHeight: '1.6' }}>{highestRisk.explanation}</p>
          </div>
          
          <div className="confidence-card" style={{ background: 'rgba(255,255,255,0.02)', padding: '20px', borderRadius: '12px' }}>
            <h3 style={{ color: '#fff', marginBottom: '15px' }}>Confidence</h3>
            <div style={{ fontSize: '2rem', color: '#8884d8', fontWeight: 'bold' }}>{highestRisk.analytics.confidence_score ? `${highestRisk.analytics.confidence_score}%` : 'N/A'}</div>
            <p style={{ color: '#aaa', fontSize: '0.9rem', marginTop: '10px' }}>{highestRisk.analytics.confidence_reason}</p>
          </div>
        </div>
      )}
      
      <PredictionForecastChart prediction={highestRisk} />

      <PredictionHistory predictions={data} />
    </div>
  );
};

export default Predictions;
