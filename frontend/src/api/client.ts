import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000',
});

// Request interceptor to add the security header
api.interceptors.request.use(
  (config) => {
    const secret = localStorage.getItem('admin_secret');
    if (secret) {
      config.headers['X-Admin-Secret'] = secret;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    return Promise.reject(error.response?.data?.detail || error.message);
  }
);

export const getLoanRecords = (limit: number = 200) => api.get('/assets/loan-records', { params: { limit } });
export const getIdentifiers = () => api.get('/assets/identifiers');

export default api;
