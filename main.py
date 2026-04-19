from fastapi import FastAPI
from datetime import datetime, timezone

# Initialize the FastAPI app
app = FastAPI(title="LLM API Assignment")

@app.get("/health")
async def health_check():
    """Returns the health status of the API."""
    return {
        "status": "ok",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }