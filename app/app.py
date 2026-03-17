from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from src.agents.orchestrator import run_agent

app = FastAPI(title="Agentic Analytics Assistant", version="1.0.0")

class AskRequest(BaseModel):
    question: str
    data_path: Optional[str] = "data/sample_metrics.csv"

class AskResponse(BaseModel):
    answer: str
    tool_used: str
    reasoning: str
    confidence: str
    success: bool

@app.get("/health")
def health(): return {"status":"ok"}

@app.post("/ask", response_model=AskResponse)
def ask(req: AskRequest):
    r = run_agent(req.question, req.data_path)
    return AskResponse(answer=r.answer,tool_used=r.tool_used,reasoning=r.reasoning,confidence=r.confidence,success=r.success)

if __name__ == "__main__":
    import uvicorn; uvicorn.run(app, host="0.0.0.0", port=8000)
