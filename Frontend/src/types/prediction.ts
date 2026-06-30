export interface RiskPrediction {
  id: number;

  workspace: number;

  node_id: string;

  risk_score: number;

  risk_level: string;

  explanation: string;

  created_at: string;

  analytics?: {
    health_trend: string;
    stability_index: string;
    stability_score: number | null;
    incident_probability: string;
    anomaly_frequency: number;
    alert_frequency: number;
    estimated_failure_window: string;
    forecast_data: number[];
    confidence_score: number;
    confidence_reason: string;
  };
}
