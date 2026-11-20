from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from backend.analyzer import analyze_lead
from backend.conversation import answer_followup

app = FastAPI(
    title="Cynbit AI Project Discovery API",
    description="Proof-of-concept API for extracting project requirements and prioritizing inquiries.",
    version="1.0.0",
)

class AnalyzeRequest(BaseModel):
    inquiry: str = Field(min_length=20, max_length=10000, description="Customer project inquiry")

@app.get("/health")
def health():
    return {"status": "ok", "service": "cynbit-ai-project-discovery"}

@app.post("/analyze")
def analyze(request: AnalyzeRequest):
    try:
        return analyze_lead(request.inquiry)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


class ChatRequest(BaseModel):
    question: str = Field(min_length=2, max_length=2000)
    original_inquiry: str = Field(min_length=20, max_length=10000)
    analysis: dict
    history: list[dict] = []

@app.post("/chat")
def chat(request: ChatRequest):
    return answer_followup(
        question=request.question,
        original_inquiry=request.original_inquiry,
        analysis=request.analysis,
        history=request.history,
    )
