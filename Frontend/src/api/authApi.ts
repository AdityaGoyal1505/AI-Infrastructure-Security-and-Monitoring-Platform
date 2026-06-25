import api from "./axios";

export const login = async (username: string, password: string) => {
  const response = await api.post("/auth/login/", { username, password });
  return response.data;
};

export const register = async (data: {
  username: string;
  email: string;
  password: string;
}) => {
  const response = await api.post("/auth/register/", data);
  return response.data;
};

export const getCurrentUser = async () => {
  const response = await api.get("/auth/me/");
  return response.data;
};
