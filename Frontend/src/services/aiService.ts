import api from "./api";

export const getAIInsights = async () => {
  const response = await api.get("/ai/insights/");
  return response.data;
};

export const getAITrends = async () => {
  const response = await api.get("/ai/trends/");
  return response.data;
};
