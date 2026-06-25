export interface RiskPrediction {
  id: number;

  workspace: number;

  node_id: string;

  risk_score: number;

  risk_level: string;

  explanation: string;

  created_at: string;
}
