export interface RiskPrediction {
  id: number;
  node_id: string;
  risk_score: number;
  risk_level: string;
  explanation: string;
}

export interface Trend {
  id: number;
  insight_type: string;
  title: string;
  occurrence_count: number;
  last_seen: string;
}
