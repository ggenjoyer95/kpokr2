import uuid
import os
from fastapi import FastAPI, UploadFile, File, HTTPException, Response

app = FastAPI()
STORAGE_DIR = "storage"
os.makedirs(STORAGE_DIR, exist_ok=True)

@app.post("/files")
async def upload_file(file: UploadFile = File(...)):
    if not file.filename.endswith(".txt"):
        raise HTTPException(status_code=400, detail="Only .txt files are allowed")
    content = await file.read()
    file_id = str(uuid.uuid4())
    path = os.path.join(STORAGE_DIR, f"{file_id}.txt")
    with open(path, "wb") as f:
        f.write(content)
    return {"file_id": file_id}

@app.get("/files/{file_id}")
def download_file(file_id: str):
    path = os.path.join(STORAGE_DIR, f"{file_id}.txt")
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="File not found")
    with open(path, "rb") as f:
        data = f.read()
    return Response(content=data, media_type="text/plain")
