/* eslint-disable @typescript-eslint/no-explicit-any */
import api from "./axios";

export const getWorkspaces = async () => {
  const response = await api.get("/workspaces/");
  return response.data;
};

export const createWorkspace = async (data: any) => {
  const response = await api.post("/workspaces/", data);
  return response.data;
};

export const updateWorkspace = async (id: number, data: any) => {
  const response = await api.put(`/workspaces/${id}/`, data);
  return response.data;
};

export const deleteWorkspace = async (id: number) => {
  const response = await api.delete(`/workspaces/${id}/`);
  return response.data;
};

export const getWorkspaceSetup = async (id: number) => {
  const response = await api.get(`/workspaces/${id}/setup/`);
  return response.data;
};
