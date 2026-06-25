/* eslint-disable @typescript-eslint/no-explicit-any */
import { useEffect, useState } from "react";

export const useWorkspaces = () => {
  const [workspaces] = useState<any[]>([]);
  const [loading] = useState(false);
  const [error] = useState<string | null>(null);

  useEffect(() => {
    // Fetch workspaces
  }, []);

  return { workspaces, loading, error };
};
