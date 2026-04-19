from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
import uvicorn

app = FastAPI(title="LLM API - Maven Assignment")

class HealthResponse(BaseModel):
    status: str
    timestamp: str

class SummarizeRequest(BaseModel):
    text: str
    max_length: int = 100

class SummarizeResponse(BaseModel):
    summary: str

@app.get("/health", response_model=HealthResponse)
async def health():
    return {
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

@app.post("/summarize", response_model=SummarizeResponse)
async def summarize(request: SummarizeRequest):
    if not request.text or len(request.text.strip()) == 0:
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    # Basic placeholder summary (will be replaced with LLM in STEP 4)
    words = request.text.split()
    summary_text = " ".join(words[:request.max_length])
    if len(words) > request.max_length:
        summary_text += "..."
    
    return {"summary": summary_text}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)