# backend/main.py
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from upload import handle_upload

from parser.mav_parser import parse_bin
from services.telemetry_store import load_log, get_metric

from agent.chat_agent import agent

from dotenv import load_dotenv
load_dotenv()


app = FastAPI()

# frontend allowed
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Backend is running. See /docs for Swagger UI."}


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

@app.get("/metric/{log_id}")
def query_metric(log_id: str, name: str):
    try:
        df = load_log(log_id)
        result = get_metric(df, name)
        return {"log_id": log_id, "metric": name, "result": result}
    except Exception as e:
        return {"error": str(e)}


@app.post("/chat")
def chat_endpoint(log_id: str, user_msg: str):
    try:
        prompt = f"Use log ID: {log_id}. User says: {user_msg}"
        response = agent.run(prompt)
        return {"response": response}
    except Exception as e:
        return {"error": str(e)}
