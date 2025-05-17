# backend/main.py
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from upload import handle_upload

from parser.mav_parser import parse_bin

app = FastAPI()

# frontend allowed
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 实际部署时应收紧
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    return await handle_upload(file)

@app.get("/parse-demo")
def demo():
    df = parse_bin("data/sample1_after PropBalance.bin")  #
    return {
        "rows": len(df),
        "fields": list(df.columns),
        "head": df.head(3).to_dict(orient="records")
    }
