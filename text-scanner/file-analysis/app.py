import os
import hashlib
import json
import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import JSONResponse

app = FastAPI()

FILE_STORING_URL = os.getenv("FILE_STORING_URL", "http://file-storing:8001")

RESULTS_DIR = "results"
os.makedirs(RESULTS_DIR, exist_ok=True)
HASH_DIR = os.path.join(RESULTS_DIR, "hashes")
os.makedirs(HASH_DIR, exist_ok=True)

class AnalyzeRequest(BaseModel):
    file_id: str

@app.post("/analyze")
def analyze_file(req: AnalyzeRequest):
    resp = requests.get(f"{FILE_STORING_URL}/files/{req.file_id}")
    if resp.status_code != 200:
        raise HTTPException(status_code=404, detail="File not found in storing service")
    content = resp.text

    paragraphs = len([p for p in content.split("\n\n") if p.strip()])
    words = len(content.split())
    chars = len(content)

    sha256 = hashlib.sha256(content.encode("utf-8")).hexdigest()
    hash_path = os.path.join(HASH_DIR, f"{sha256}.txt")

    similarity = 100 if os.path.exists(hash_path) else 0

    if similarity == 0:
        with open(hash_path, "w", encoding="utf-8") as hf:
            hf.write(content)

    result = {
        "file_id": req.file_id,
        "paragraphs": paragraphs,
        "words": words,
        "chars": chars,
        "similarity": similarity,
    }

    out_path = os.path.join(RESULTS_DIR, f"{req.file_id}.json")
    with open(out_path, "w", encoding="utf-8") as rf:
        json.dump(result, rf)

    return JSONResponse(result)

@app.get("/analyze/{file_id}")
def get_analysis(file_id: str):
    path = os.path.join(RESULTS_DIR, f"{file_id}.json")
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Analysis not found")
    with open(path, "r", encoding="utf-8") as rf:
        data = json.load(rf)
    return JSONResponse(data)
