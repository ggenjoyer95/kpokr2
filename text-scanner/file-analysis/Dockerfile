FROM python:3.11-slim

WORKDIR /app

# Копируем приложение
COPY app.py ./

# Устанавливаем зависимости
RUN pip install fastapi uvicorn requests

# Создаём папки для результатов
RUN mkdir -p results hashes

EXPOSE 8002

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8002"]
