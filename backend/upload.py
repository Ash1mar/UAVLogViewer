# backend/upload.py
import uuid
import os
from fastapi import UploadFile
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

async def handle_upload(file: UploadFile):
    log_id = str(uuid.uuid4())
    dest = DATA_DIR / f"{log_id}.bin"

    with open(dest, "wb") as f:
        content = await file.read()
        f.write(content)

    return {
        "message": "upload successful",
        "log_id": log_id,
        "filename": file.filename
    }
