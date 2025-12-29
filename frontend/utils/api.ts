import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001';

// Create axios instance
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests if available
api.interceptors.request.use(
  (config) => {
    if (typeof window !== 'undefined') {
      const token = localStorage.getItem('token');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Handle 401 errors (unauthorized)
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expired or invalid
      if (typeof window !== 'undefined') {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        window.location.href = '/auth/login';
      }
    }
    return Promise.reject(error);
  }
);

export default api;

// Auth API
export const authAPI = {
  register: (data: { name: string; email: string; password: string }) =>
    api.post('/api/auth/register', data),
  login: (data: { email: string; password: string }) =>
    api.post('/api/auth/login/json', data),
  getCurrentUser: () => api.get('/api/auth/me'),
};

// Issues API
export const issuesAPI = {
  getAll: (params?: {
    skip?: number;
    limit?: number;
    category?: string;
    status?: string;
  }) => api.get('/api/issues/', { params }),
  getById: (id: number) => api.get(`/api/issues/${id}`),
  create: (data: FormData) =>
    api.post('/api/issues/', data, {
      headers: { 'Content-Type': 'multipart/form-data' },
    }),
  update: (id: number, data: any) => api.patch(`/api/issues/${id}`, data),
  updateStatus: (id: number, status: string) =>
    api.put(`/api/issues/${id}/status?new_status=${status}`),
  delete: (id: number) => api.delete(`/api/issues/${id}`),
};

// Notifications API
export const notificationsAPI = {
  getAll: (params?: { skip?: number; limit?: number; unread_only?: boolean }) =>
    api.get('/api/notifications/', { params }),
  getUnreadCount: () => api.get('/api/notifications/unread/count'),
  markAsRead: (id: number) => api.put(`/api/notifications/${id}/read`),
  markAllAsRead: () => api.put('/api/notifications/read-all'),
};

