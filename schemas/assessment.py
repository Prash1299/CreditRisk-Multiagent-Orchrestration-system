from typing import Any, Literal

from pydantic import BaseModel, Field

Disposition = Literal["suitable", "refer", "not_suitable"]


class AssessmentRequest(BaseModel):
    request: str = Field(
        ...,
        examples=[
            "I earn ₹85,000 per month, have an existing EMI of ₹15,000, "
            "a credit score of 720, and want a personal loan of ₹8 lakh for 4 years."
        ],
    )
    session_id: str = Field(default="default")
    borrower_id: str | None = None
    async_mode: bool = False


class AssessmentResponse(BaseModel):
    session_id: str
    applicant: dict[str, Any]
    disposition: Disposition | None = None
    risk_score: float | None = None
    probability_of_default: float | None = None
    recommendations: list[dict[str, Any]] = Field(default_factory=list)
    rationale: str | None = None
    research: dict[str, Any] = Field(default_factory=dict)
    analysis: dict[str, Any] = Field(default_factory=dict)
    review: dict[str, Any] = Field(default_factory=dict)
    plan: list[dict[str, Any]] = Field(default_factory=list)
    disclaimer: str
    job_id: str | None = None
    status: str = "completed"


class JobStatus(BaseModel):
    job_id: str
    status: str
    result: AssessmentResponse | None = None
    error: str | None = None
