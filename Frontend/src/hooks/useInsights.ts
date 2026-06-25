/* eslint-disable @typescript-eslint/no-explicit-any */
import { useEffect, useState } from "react";

export const useInsights = (workspaceId: string) => {
  const [insights] = useState<any[]>([]);
  const [loading] = useState(false);
  const [error] = useState<string | null>(null);

  useEffect(() => {
    if (workspaceId) {
      // Fetch insights
    }
  }, [workspaceId]);

  return { insights, loading, error };
};
