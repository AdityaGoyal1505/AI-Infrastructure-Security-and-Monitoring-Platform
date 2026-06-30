export interface Trend {
  id: number;

  workspace: number;

  insight_type: string;

  title: string;

  description: string;

  occurrence_count: number;

  created_at: string;

  analytics?: {
    most_affected_nodes: { node_id: string; count: number }[];
    metric_drift: Record<string, number>;
    overall_stability: number;
  };
}
