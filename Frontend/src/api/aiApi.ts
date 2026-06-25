import type { DashboardData } from "../types/dashboard";
import api from "./axios";

export const getAIInsights = async (
  workspaceId: number,
): Promise<DashboardData> => {
  const response = await api.get("/ai/insights/", {
    params: { workspace: workspaceId },
  });
  return response.data;
};

export const askAI = async (
  workspace: number,

  question: string,
) => {
  const response = await api.post(
    "/ai/chat/",

    {
      workspace,

      question,
    },
  );

  return response.data;
};