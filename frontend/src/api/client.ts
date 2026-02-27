import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || (import.meta.env.PROD ? '/api' : 'http://localhost:8000'),
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
export const getOTPCount = () => api.get('/admin/otp/count');
export const addSingleOTP = (password: string) => api.post('/admin/otp/single', { password });
export const uploadOTPBatch = (file: File) => {
  const formData = new FormData();
  formData.append('file', file);
  return api.post('/admin/otp/batch', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  });
};

export default api;
