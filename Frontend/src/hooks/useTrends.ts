/* eslint-disable @typescript-eslint/no-explicit-any */
import { useEffect, useState } from "react";

import { getTrends } from "../api/trendsApi";

import type { Trend } from "../types/trends";

import { useWorkspace } from "../context/WorkspaceContext";

const useTrends = () => {
  const { workspace } = useWorkspace();

  const [data, setData] = useState<Trend[]>([]);

  const [loading, setLoading] = useState(true);

  const [error, setError] = useState("");

  useEffect(() => {
    const fetchTrends = async () => {
      try {
        if (!workspace.id) {
          setLoading(false);

          return;
        }

        setLoading(true);

        setError("");

        const response = await getTrends(workspace.id);

        setData(response);
      } catch (err: any) {
        setError(err?.response?.data?.detail || "Failed to fetch trends");
      } finally {
        setLoading(false);
      }
    };

    fetchTrends();
  }, [workspace.id]);

  const topInsight = data.length > 0 ? data[0] : null;

  return {
    data,

    loading,

    error,

    topInsight,
  };
};

export default useTrends;
