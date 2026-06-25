import api from "./axios";

export const getPredictions = async (workspaceId: number) => {
  const response = await api.get("/ai/predictions/", {
    params: { workspace: workspaceId },
  });
  return response.data;
};
