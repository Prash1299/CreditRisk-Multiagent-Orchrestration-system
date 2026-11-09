from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from database.db import save_assessment
from graph.workflow import compile_graph
from memory.long_term import LongTermMemory

app = FastAPI(title="CreditRisk Multi-Agent API")
graph = compile_graph()
memory = LongTermMemory()


class AssessmentRequest(BaseModel):
    borrower_id: str = Field(..., examples=["B001"])
    product_id: str = Field(..., examples=["P200"])
    request: str = "Assess this credit application."


class AssessmentResponse(BaseModel):
    borrower_id: str
    product_id: str
    risk_score: float | None
    recommendation: str | None
    rationale: str | None
    research: dict
    analysis: dict
    review: dict


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/assess", response_model=AssessmentResponse)
def assess(payload: AssessmentRequest) -> AssessmentResponse:
    result = graph.invoke(
        {
            "borrower_id": payload.borrower_id,
            "product_id": payload.product_id,
            "request": payload.request,
            "messages": [{"role": "user", "content": payload.request}],
        }
    )
    research = result.get("research") or {}
    if not research.get("borrower"):
        raise HTTPException(status_code=404, detail="Borrower not found")
    if not research.get("product"):
        raise HTTPException(status_code=404, detail="Loan product not found")

    save_assessment(
        payload.borrower_id,
        payload.product_id,
        result.get("risk_score"),
        result.get("recommendation"),
        result.get("rationale"),
    )
    memory.store(
        {
            "borrower_id": payload.borrower_id,
            "product_id": payload.product_id,
            "recommendation": result.get("recommendation"),
            "risk_score": result.get("risk_score"),
            "industry": (research.get("borrower") or {}).get("industry"),
        }
    )
    return AssessmentResponse(
        borrower_id=payload.borrower_id,
        product_id=payload.product_id,
        risk_score=result.get("risk_score"),
        recommendation=result.get("recommendation"),
        rationale=result.get("rationale"),
        research=research,
        analysis=result.get("analysis") or {},
        review=result.get("review") or {},
    )
