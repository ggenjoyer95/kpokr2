FROM python:3.11-slim

WORKDIR /app

# Делаем storage томом
VOLUME ["/app/storage"]

COPY app.py ./

RUN pip install fastapi uvicorn python-multipart

EXPOSE 8001

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8001"]
