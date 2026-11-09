from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from core.constants import DISCLAIMER
from database.db import init_db
from graph.pipeline import run_assessment
from schemas.assessment import AssessmentRequest, AssessmentResponse, JobStatus

app = FastAPI(
    title="CreditRisk Multi-Agent",
    description="Decision-support orchestration for credit risk and loan recommendations.",
    version="0.2.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup() -> None:
    init_db()


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "disclaimer": DISCLAIMER}


@app.post("/assess", response_model=AssessmentResponse | JobStatus)
def assess(payload: AssessmentRequest):
    if payload.async_mode:
        try:
            from worker.tasks import assess_task
        except Exception as exc:
            raise HTTPException(status_code=503, detail=f"Celery unavailable: {exc}") from exc
        task = assess_task.delay(payload.request, payload.session_id, payload.borrower_id)
        return JobStatus(job_id=task.id, status="queued")
    return run_assessment(payload.request, payload.session_id, payload.borrower_id)


@app.get("/jobs/{job_id}", response_model=JobStatus)
def job_status(job_id: str) -> JobStatus:
    try:
        from worker.celery_app import celery_app
    except Exception as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    async_result = celery_app.AsyncResult(job_id)
    if async_result.successful():
        return JobStatus(
            job_id=job_id,
            status="completed",
            result=AssessmentResponse.model_validate(async_result.result),
        )
    if async_result.failed():
        return JobStatus(job_id=job_id, status="failed", error=str(async_result.result))
    return JobStatus(job_id=job_id, status=async_result.status or "pending")
