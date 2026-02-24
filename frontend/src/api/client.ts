import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000',
});

// Response interceptor to handle errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    return Promise.reject(error.response?.data?.detail || error.message);
  }
);

export default api;
