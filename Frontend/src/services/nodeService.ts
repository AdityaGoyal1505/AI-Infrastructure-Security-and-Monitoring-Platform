import api from "./api";

export const getNodes = async () => {
  const response = await api.get("/nodes/");
  return response.data;
};
