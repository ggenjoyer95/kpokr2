
Контрольная работа 2

Автор: Приладышев Юрий
Группа: 238

Описание:
Микросервисное веб-приложение для анализа текстовых отчётов
  - статистика (абзацы, слова, символы)
  - выявление 100% совпадений (антиплагиат)
  - (опционально) облако слов через QuickChart Word-Cloud API

Стек:
  Python 3.11
  FastAPI + Uvicorn
  requests (HTTP-клиент)
  python-multipart (обработка форм)
  Docker, Docker Compose
  pytest + pytest-cov (тестирование)

Запуск:
Собрать и поднять все сервисы:
   docker-compose up --build -d 

Проверить, что сервисы поднялись:
   docker-compose ps

Описание сервисов:
1) API Gateway (8000) — единая точка входа, проксирует:
   POST /files      → File Storing Service
   GET  /files/{id} → File Storing Service
   POST /analyze    → File Analysis Service
   GET  /analyze/{id} → File Analysis Service

2) File Storing Service (8001) — приём и выдача .txt:
   POST /files       (multipart/form-data; только .txt)
     → { "file_id": "<UUID>" }
   GET  /files/{id}  (plain text или 404)

3) File Analysis Service (8002) — анализ и хранение результатов:
   POST /analyze     { "file_id": "<UUID>" }
     → { "file_id":..., "paragraphs":..., "words":..., "chars":..., "similarity":... }
   GET  /analyze/{id} (возвращает тот же JSON или 404)

Примеры использования:
  # Загрузка
  curl -F "file=@report.txt" http://localhost:8000/files

  # Анализ
  curl -X POST -H "Content-Type: application/json" \
       -d '{"file_id":"<UUID>"}' \
       http://localhost:8000/analyze

  # Получение результата
  curl http://localhost:8000/analyze/<UUID>

  # Скачивание оригинала
  curl http://localhost:8000/files/<UUID> -o downloaded.txt

Документация API (Swagger UI):
  Gateway: http://localhost:8000/docs
  Storing: http://localhost:8001/docs
  Analysis: http://localhost:8002/docs
