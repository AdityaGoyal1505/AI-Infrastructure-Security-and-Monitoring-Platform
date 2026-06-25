import type { RiskPrediction } from "../types/prediction";
import api from "./axios";

export const getPredictions = async (
  workspaceId: number,
): Promise<RiskPrediction[]> => {
  const response = await api.get("/ai/predictions/", {
    params: {
      workspace: workspaceId,
    },
  });
  return response.data;
};
