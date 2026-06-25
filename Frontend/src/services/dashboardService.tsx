import api from "./api";

export const getDashboardData = async () => {
  const response = await api.get("/ai/insights/");
  return response.data;
};

export const getAlerts = async () => {
  const response = await api.get("/alerts/");
  return response.data;
};

export const getIncidents = async () => {
  const response = await api.get("/incidents/");
  return response.data;
};

export const getNodes = async () => {
  const response = await api.get("/nodes/");
  return response.data;
};
