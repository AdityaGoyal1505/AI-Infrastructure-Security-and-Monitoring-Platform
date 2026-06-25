export interface HealthScore {
  score: number;
  status: string;
}

export interface RootCauseAnalysis {
  root_cause: string;
  summary: string;
  confidence: number;
  recommendations: string[];
}

export interface Recommendation {
  id: number;
  title: string;
  description: string;
  priority: string;
}

export interface Anomaly {
  id: number;
  metric_name: string;
  observed_value: number;
  baseline_value: number;
  anomaly_score: number;
  created_at: string;
}

export interface Insight {
  id: number;
  insight_type: string;
  title: string;
  description: string;
  occurrence_count: number;
}

export interface RiskPrediction {
  risk_score: number;
  risk_level: string;
  explanation: string;
}

export interface DashboardData {
  latest_rca: RootCauseAnalysis | null;
  health_score: HealthScore | null;
  recommendations: Recommendation[];
  recent_anomalies: Anomaly[];
  top_insights: Insight[];
  alerts_count: number;
  anomaly_count: number;
  risk_prediction: RiskPrediction | null;
}
