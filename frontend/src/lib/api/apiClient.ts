import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000', // Важно: порт 8000
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Добавляем интерсептор для логирования
api.interceptors.request.use((config) => {
  console.log(`Отправка запроса на ${config.baseURL}${config.url}`);
  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('Ошибка запроса:', error.config.url, error.response?.status);
    return Promise.reject(error);
  }
);

export default api;