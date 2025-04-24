# Используем официальный Node.js образ
FROM node:20-alpine

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем package.json и package-lock.json
COPY package*.json ./

# Устанавливаем зависимости
RUN npm install

# Копируем остальные файлы проекта
COPY . .

# Собираем проект Vite
RUN npm run build

# Устанавливаем сервер для продакшена
RUN npm install -g serve

# Запускаем собранное приложение
CMD ["serve", "-s", "dist"]
