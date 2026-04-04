import axios from "axios";

const API = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || "http://localhost:8001",
});

// Auto-attach JWT token to every request
API.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

export default API;

export const auth = {
  register: (data: any) => API.post("/auth/register", data),
  login: (data: any)    => API.post("/auth/login", data),
};

export const orders = {
  list:   ()          => API.get("/orders/"),
  create: (data: any) => API.post("/orders/", data),
  get:    (id: string) => API.get(`/orders/${id}`),
  updateStatus: (id: string, status: string) =>
    API.patch(`/orders/${id}/status`, { status }),
};

export const drivers = {
  list:   ()      => API.get("/drivers/"),
  assign: (data: any) => API.post("/drivers/assign", data),
};

export const routes = {
  surge: (data: any) => API.post("/routes/surge", data),
};