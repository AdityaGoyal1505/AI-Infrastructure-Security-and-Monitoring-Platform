import api from "./axios";

export const downloadAgent = async (workspaceId: number) => {
  try {
    const response = await api.get(
      `/workspaces/${workspaceId}/agent/`,

      {
        responseType: "blob",
      },
    );

    const url = window.URL.createObjectURL(response.data);

    const link = document.createElement("a");

    link.href = url;

    link.download = "monitoring-agent.zip";

    document.body.appendChild(link);

    link.click();

    document.body.removeChild(link);

    window.URL.revokeObjectURL(url);
  } catch (error) {
    console.error(
      "Failed to download agent:",

      error,
    );

    throw error;
  }
};

export const getWorkspaceSetup = async (workspaceId: number) => {
  try {
    const response = await api.get(`/workspaces/${workspaceId}/setup/`);

    return response.data;
  } catch (error) {
    console.error(
      "Failed to fetch workspace setup:",

      error,
    );

    throw error;
  }
};
