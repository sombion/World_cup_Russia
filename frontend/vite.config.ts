import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000', // Все запросы на /api перенаправляем на бэкенд
        changeOrigin: true,
        secure: false,
      }
    }
  }
});