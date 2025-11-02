
# Используем официальный образ Python (версия 3.9, облегчённый)
FROM python:3.9-slim


# Устанавливаем рабочую директорию в контейнере
WORKDIR /app


# Копируем requirements.txt в контейнер
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt


# Копируем остальной код проекта
COPY main.py .

# Открываем порт (если приложение веб‑сервер, например Flask)
EXPOSE 8080

# Команда для запуска приложения
CMD ["python", "main.py"]