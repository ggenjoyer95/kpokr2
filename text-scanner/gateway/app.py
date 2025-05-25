import os
import requests
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi import UploadFile, File

app = FastAPI()

# URL-адреса микросервисов внутри сети Docker Compose
FILE_STORING_URL = os.getenv("FILE_STORING_URL", "http://file-storing:8001")
FILE_ANALYSIS_URL = os.getenv("FILE_ANALYSIS_URL", "http://file-analysis:8002")

@app.post("/files")
async def upload_file(file: UploadFile = File(...)):
    # Проксируем загрузку файлов
    files = {"file": (file.filename, await file.read(), file.content_type)}
    resp = requests.post(f"{FILE_STORING_URL}/files", files=files)
    if resp.status_code != 200:
        raise HTTPException(status_code=resp.status_code, detail=resp.text)
    return JSONResponse(resp.json(), status_code=resp.status_code)

@app.get("/files/{file_id}")
def download_file(file_id: str):
    # Проксируем скачивание файлов
    resp = requests.get(f"{FILE_STORING_URL}/files/{file_id}")
    if resp.status_code != 200:
        raise HTTPException(status_code=resp.status_code, detail=resp.text)
    return Response(content=resp.content, media_type="text/plain")

@app.post("/analyze")
def analyze(req: dict):
    # Проксируем запрос на анализ
    resp = requests.post(f"{FILE_ANALYSIS_URL}/analyze", json=req)
    if resp.status_code != 200:
        raise HTTPException(status_code=resp.status_code, detail=resp.text)
    return JSONResponse(resp.json(), status_code=resp.status_code)

@app.get("/analyze/{file_id}")
def get_analysis(file_id: str):
    # Проксируем получение результатов анализа
    resp = requests.get(f"{FILE_ANALYSIS_URL}/analyze/{file_id}")
    if resp.status_code != 200:
        raise HTTPException(status_code=resp.status_code, detail=resp.text)
    return JSONResponse(resp.json(), status_code=resp.status_code)
