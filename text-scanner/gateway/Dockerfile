# Используем официальный образ Python
FROM python:3.11-slim

WORKDIR /app

# Копируем приложение
COPY app.py ./

# Ставим зависимости
RUN pip install fastapi uvicorn

# Открываем порт
EXPOSE 8000

# Запускаем
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
