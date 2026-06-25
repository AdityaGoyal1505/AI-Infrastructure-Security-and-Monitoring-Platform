import api from "./axios";

import type { Trend } from "../types/trends";

export const getTrends = async (workspaceId: number): Promise<Trend[]> => {
  const response = await api.get(
    "/ai/trends/",

    {
      params: {
        workspace: workspaceId,
      },
    },
  );

  return response.data;
};
