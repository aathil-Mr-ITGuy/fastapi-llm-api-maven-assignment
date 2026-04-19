from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
import uvicorn
import os
import json
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
    sentiment: str   # "positive" | "negative" | "neutral"
    confidence: float
    explanation: str

@app.get("/health", response_model=HealthResponse)
async def health():
    return {
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

# === Summarize function (unchanged from before) ===
def summarize_with_prompt(text: str, max_length: int, version: int = 2) -> str:
    if version == 1:
        prompt = f"""Summarize the following text in {max_length} words or less. Be concise and capture the main points only.\n\nText: {text}\n\nSummary:"""
    elif version == 2:
        prompt = f"""You are an expert summarizer. Create a clear, professional summary of the text below. Limit to approximately {max_length} words. Focus on key ideas.\n\nText: {text}\n\nSummary:"""
    else:
        prompt = f"""Provide a high-quality, coherent summary of this text in no more than {max_length} words. Make it readable and natural.\n\nText: {text}\n\nSummary:"""

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

# === FIXED: 3 Prompt Variations for Sentiment Analysis ===
def analyze_sentiment_with_prompt(text: str, version: int = 2) -> dict:
    base_instructions = """You are a precise sentiment analysis expert.
Return ONLY a valid JSON object with these exact keys:
- "sentiment": one of "positive", "negative", or "neutral"
- "confidence": a float number between 0.0 and 1.0
- "explanation": a short clear reason (max 120 characters)

Do not add any extra text, explanation, or markdown outside the JSON."""

    if version == 1:
        prompt = f"""{base_instructions}

Text: {text}

JSON:"""
    elif version == 2:
        prompt = f"""{base_instructions}

Analyze the emotional tone carefully and be objective.

Text: {text}

JSON:"""
    else:  # version 3 - strongest
        prompt = f"""{base_instructions}

Be very accurate with confidence score.

Text: {text}

JSON:"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=250,
            temperature=0.1,
            response_format={"type": "json_object"}   # This forces JSON output
        )
        
        result_text = response.choices[0].message.content.strip()
        
        # Parse JSON safely
        result = json.loads(result_text)
        
        return {
            "sentiment": str(result.get("sentiment", "neutral")).lower(),
            "confidence": float(result.get("confidence", 0.5)),
            "explanation": str(result.get("explanation", "No explanation provided."))
        }
        
    except Exception as e:
        # Robust fallback
        return {
            "sentiment": "neutral",
            "confidence": 0.5,
            "explanation": f"Parsing error occurred. Raw response: {str(e)[:80]}"
        }

@app.post("/analyze-sentiment", response_model=SentimentResponse)
async def analyze_sentiment(request: SentimentRequest):
    if not request.text or len(request.text.strip()) == 0:
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    result = analyze_sentiment_with_prompt(request.text, version=2)
    return result

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)