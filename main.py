from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
import uvicorn
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
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

class SentimentRequest(BaseModel):
    text: str

class SentimentResponse(BaseModel):
    sentiment: str  # "positive" | "negative" | "neutral"
    confidence: float  # 0.0 to 1.0
    explanation: str

@app.get("/health", response_model=HealthResponse)
async def health():
    return {
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

# === Summarize with 3 Prompt Variations (from STEP 4) ===
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
    
    summary = summarize_with_prompt(request.text, request.max_length, version=2)
    return {"summary": summary}

# === Basic Sentiment Analysis (placeholder - will be improved in STEP 6) ===
@app.post("/analyze-sentiment", response_model=SentimentResponse)
async def analyze_sentiment(request: SentimentRequest):
    if not request.text or len(request.text.strip()) == 0:
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    # Basic placeholder logic (will be replaced with LLM in next step)
    text_lower = request.text.lower()
    if any(word in text_lower for word in ["good", "great", "excellent", "happy", "love", "amazing"]):
        sentiment = "positive"
        confidence = 0.75
        explanation = "Detected positive keywords in the text."
    elif any(word in text_lower for word in ["bad", "terrible", "awful", "sad", "hate", "worst"]):
        sentiment = "negative"
        confidence = 0.70
        explanation = "Detected negative keywords in the text."
    else:
        sentiment = "neutral"
        confidence = 0.60
        explanation = "No strong positive or negative keywords detected."
    
    return {
        "sentiment": sentiment,
        "confidence": confidence,
        "explanation": explanation
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)