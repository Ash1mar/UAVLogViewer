# ✈️ UAVLogViewer + Agentic Chatbot (Backend Take‑Home)

Forked from [ArduPilot/UAVLogViewer](https://github.com/ArduPilot/UAVLogViewer) and extended with a **Python FastAPI backend** that parses `.bin` flight logs and provides an LLM‑powered chatbot for investigative Q & A.

---

## Features

| Module | Highlights |
|--------|------------|
| **FastAPI backend** | `/upload` (log upload) · `/metric/{log_id}` (quick stats) · `/chat` (LLM chat) |
| **MAVLink parser** | `pymavlink` → `pandas.DataFrame` (GPS, ALT, BAT, ERR …) |
| **LangChain agent** | Tools for altitude, GPS loss, battery, flight time, error list |
| **Anomaly detector** | Voltage sag · GPS fix loss · sudden altitude drop |
| **Session memory** | Chat agent remembers context, can ask clarifying questions |

---

## Quick Start (Local)

### 1. Clone & create virtualenv

```bash
git clone https://github.com/<your-username>/UAVLogViewer.git
cd UAVLogViewer/backend
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install backend dependencies

```bash
pip install -r requirements.txt
```

### 3. Add your OpenAI key

```bash
cp .env.example .env          # then edit .env
# OPENAI_API_KEY=sk-********************************
```

### 4. Run backend (auto‑reload)

```bash
uvicorn main:app --reload
```

- API docs: <http://localhost:8000/docs>  
- Health check: <http://localhost:8000/health>

---

## API Walk‑Through

1. **Upload log**

   `POST /upload` → form‑data `file=<your_log>.bin`

   ```json
   {
     "log_id": "e9ac0a32-306b-4b09-93a7-bb76a8c2dcd3",
     "message": "upload successful"
   }
   ```

2. **Quick metric**

   `GET /metric/{log_id}?name=max_altitude` → `134.2`

3. **Chatbot**

   `POST /chat`
   ```json
   {
     "log_id": "e9ac0a32-306b-4b09-93a7-bb76a8c2dcd3",
     "user_msg": "What was the highest altitude?"
   }
   ```
   Response example:

   ```
   The highest altitude recorded was **134 m**.
   ```

   Supported sample questions:

   - “When did the GPS signal first get lost?”
   - “How long was the total flight time?”
   - “List all critical errors that happened mid‑flight.”
   - “Are there any anomalies in this flight?”

---

## Repo Layout

```
backend/
├─ main.py              ← FastAPI entry
├─ upload.py            ← /upload handler
├─ parser/              ← .bin → DataFrame
├─ services/            ← cache + metric helpers
└─ agents/              ← tools & LangChain agent
frontend/               ← original Vue viewer (unchanged)
```

---

## Running Frontend (optional)

```bash
cd frontend   # project root
npm install
npm run dev   # http://localhost:8080
```

---

## Next Steps / Ideas
 
- Docker‑compose one‑click stack   
- Vue chat widget embedded next to plot
