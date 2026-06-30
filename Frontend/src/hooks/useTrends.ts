/* eslint-disable @typescript-eslint/no-explicit-any */
/* eslint-disable @typescript-eslint/no-explicit-any */
import { useEffect, useState } from "react";

import { getTrends } from "../api/trendsApi";
import type { Trend } from "../types/trends";
import { useWorkspace } from "../context/WorkspaceContext";

interface ExecutiveMetrics {
  overall_trend: string;
  avg_health_score: number | null;
  active_anomalies: number;
  risk_trend: string;
  stability: string;
  explanation: string;
}

interface AITrendResponse {
  summary: { 
    executive: string;
    executive_metrics?: ExecutiveMetrics;
  };
  single_node: boolean;
  charts: {
    health_score: { timestamp: string; score: number }[];
    alerts: { timestamp: string; count: number }[];
    anomalies: { timestamp: string; count: number }[];
    risk: { timestamp: string; risk_score: number }[];
    stability: { timestamp: string; stability: number }[];
    pattern_distribution: { pattern: string; count: number }[];
    top_affected_nodes?: any[];
  };
  timeline?: {
    type: string;
    title: string;
    severity: string;
    node: string;
    description: string;
    timestamp: string;
  }[];
  // other fields omitted for brevity
}

const useTrends = () => {
  const { workspace } = useWorkspace();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [trendData, setTrendData] = useState<AITrendResponse | null>(null);

  useEffect(() => {
    const fetchTrends = async () => {
      if (!workspace.id) {
        setLoading(false);
        return;
      }
      setLoading(true);
      setError("");
      try {
        const response = await getTrends(workspace.id);
        setTrendData(response as unknown as AITrendResponse);
      } catch (err: any) {
        setError(err?.response?.data?.detail || "Failed to fetch trends");
      } finally {
        setLoading(false);
      }
    };
    fetchTrends();
  }, [workspace.id]);

  // Derive a flat array of Trend objects for legacy components (if needed)
  const legacyData: Trend[] = [];
  if (trendData) {
    // Transform the health_score chart into Trend-like objects for compatibility
    legacyData.push(
      ...trendData.charts.health_score.map((hs) => ({
        id: 0,
        workspace: workspace.id,
        insight_type: "health_score",
        title: "Health Score",
        description: "",
        occurrence_count: hs.score,
        created_at: hs.timestamp,
        analytics: undefined,
      }))
    );
  }

  return {
    loading,
    error,
    data: legacyData,
    executiveSummary: trendData?.summary.executive ?? "",
    executiveMetrics: trendData?.summary.executive_metrics ?? null,
    singleNode: trendData?.single_node ?? false,
    charts: trendData?.charts ?? null,
    timeline: trendData?.timeline ?? [],
    trendData: trendData ?? null
  };
};

export default useTrends;
