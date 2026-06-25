import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000/api",

  withCredentials: true,

  headers: {
    "Content-Type": "application/json",
  },
});

api.interceptors.response.use(
  (response) => response,

  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        await api.post("/auth/refresh/");

        return api(originalRequest);
      } catch {
        localStorage.clear();

        window.location.href = "/auth";
      }
    }

    return Promise.reject(error);
  }
);

export default api;