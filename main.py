from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
import uvicorn
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = FastAPI(title="LLM API - Maven Assignment")

# Initialize OpenAI client
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY is not set in .env file")

client = OpenAI(api_key=api_key)

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

# === 3 Prompt Variations for Summarization ===
def summarize_with_prompt(text: str, max_length: int, version: int = 2) -> str:
    if version == 1:
        prompt = f"""Summarize the following text in {max_length} words or less. 
Be concise and capture the main points only.

Text: {text}

Summary:"""
    elif version == 2:
        prompt = f"""You are an expert summarizer. Create a clear, professional summary of the text below. 
Limit the summary to approximately {max_length} words. Focus on key ideas and remove fluff.

Text: {text}

Summary:"""
    elif version == 3:
        prompt = f"""Provide a high-quality, coherent summary of this text in no more than {max_length} words. 
Make it readable and natural. Prioritize the most important information.

Text: {text}

Summary:"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300,
        temperature=0.3
    )
    return response.choices[0].message.content.strip()

@app.post("/summarize", response_model=SummarizeResponse)
async def summarize(request: SummarizeRequest):
    if not request.text or len(request.text.strip()) == 0:
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    summary = summarize_with_prompt(request.text, request.max_length, version=3)
    return {"summary": summary}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)