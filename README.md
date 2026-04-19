Here’s the clean **README.md** content ready for easy copy-paste into your file (or directly into Canvas if needed):

```markdown
# FastAPI LLM API - Maven Assignment

A FastAPI-based REST API that provides text summarization and sentiment analysis using OpenAI's GPT-4o-mini model.

## Features
- Health check endpoint
- Text summarization with prompt engineering
- Sentiment analysis with prompt engineering
- Pydantic models for validation
- Basic error handling
- Deployed on Render (free tier)

## Endpoints

### 1. GET /health
Returns API health status.

**Response:**
```json
{
  "status": "ok",
  "timestamp": "2026-04-19T13:45:30.123456Z"
}
```

### 2. POST /summarize
Summarizes input text.

**Request Body:**
```json
{
  "text": "Your long text here...",
  "max_length": 100
}
```

**Response:**
```json
{
  "summary": "Short and clear summary..."
}
```

### 3. POST /analyze-sentiment
Analyzes sentiment of the given text.

**Request Body:**
```json
{
  "text": "I absolutely love this new AI tool!"
}
```

**Response:**
```json
{
  "sentiment": "positive",
  "confidence": 0.85,
  "explanation": "Strong positive language and enthusiasm detected."
}
```

## Prompt Engineering

### Summarization (3 Prompt Variations Tested)
- **Version 1**: Simple concise prompt
- **Version 2**: Expert summarizer role (Best)
- **Version 3**: High-quality natural language prompt

**Best Prompt**: Version 2 – Produces clear, professional, and well-structured summaries.

### Sentiment Analysis (3 Prompt Variations Tested)
- **Version 1**: Basic structured JSON
- **Version 2**: Expert with objective tone (Best)
- **Version 3**: Strict JSON with high accuracy focus

**Best Prompt**: Version 2 – Most consistent sentiment labels and reasonable confidence scores.

## Tech Stack
- Python + FastAPI
- OpenAI (gpt-4o-mini)
- Pydantic
- Uvicorn
- Deployed on Render

## Local Setup

```bash
git clone https://github.com/aathil-Mr-ITGuy/fastapi-llm-api-maven-assignment.git
cd fastapi-llm-api-maven-assignment

python -m venv venv
venv\Scripts\activate     # On Windows

pip install -r requirements.txt

# Create .env file and add your OpenAI key
echo OPENAI_API_KEY=sk-your-key > .env

python main.py
```

Access Swagger UI at: `http://127.0.0.1:8000/docs`

## Live Deployment
**Deployed URL**: https://fastapi-llm-api-maven-assignment.onrender.com/

**Swagger UI**: https://fastapi-llm-api-maven-assignment.onrender.com/docs

## Repository
https://github.com/aathil-Mr-ITGuy/fastapi-llm-api-maven-assignment.git
