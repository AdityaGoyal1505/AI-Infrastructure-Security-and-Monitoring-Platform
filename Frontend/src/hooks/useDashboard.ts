/* eslint-disable react-hooks/set-state-in-effect */
import { useEffect, useState } from "react";
import { getAIInsights } from "../api/aiApi";
import { useWorkspace } from "../context/WorkspaceContext";
import type { DashboardData } from "../types/dashboard";

export const useDashboard = () => {
  const { workspace } = useWorkspace();

  const [data, setData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!workspace?.id) {
      setLoading(false);
      return;
    }

    const fetchData = async () => {
      if (!workspace?.id) return;
      try {
        setLoading(true);
        const response = await getAIInsights(workspace.id);
        setData(response);
        setError("");
      } catch (err) {
        console.error(err);
        setError("Failed to fetch dashboard data");
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [workspace]);

  return { data, loading, error };
};
