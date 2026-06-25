/* eslint-disable @typescript-eslint/no-explicit-any */
import { useEffect, useState } from "react";

import { getPredictions } from "../api/predictionsApi";

import type { RiskPrediction } from "../types/prediction";

import { useWorkspace } from "../context/WorkspaceContext";

const usePredictions = () => {
  const { workspace } = useWorkspace();

  const [data, setData] = useState<RiskPrediction[]>([]);

  const [loading, setLoading] = useState(true);

  const [error, setError] = useState("");

  useEffect(() => {
    const fetchPredictions = async () => {
      try {
        if (!workspace.id) {
          setLoading(false);

          return;
        }

        setLoading(true);

        setError("");

        const response = await getPredictions(workspace.id);

        setData(response);
      } catch (err: any) {
        console.error(err);

        setError(err?.response?.data?.detail || "Failed to fetch predictions");
      } finally {
        setLoading(false);
      }
    };

    fetchPredictions();
  }, [workspace.id]);

  const highestRisk = data.length > 0 ? data[0] : null;

  const highRiskNodes = data.filter((item) => item.risk_level === "HIGH");

  const mediumRiskNodes = data.filter((item) => item.risk_level === "MEDIUM");

  const lowRiskNodes = data.filter((item) => item.risk_level === "LOW");

  return {
    data,

    loading,

    error,

    highestRisk,

    highRiskNodes,

    mediumRiskNodes,

    lowRiskNodes,
  };
};

export default usePredictions;
