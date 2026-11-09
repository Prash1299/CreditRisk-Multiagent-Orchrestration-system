from __future__ import annotations

import json
from functools import lru_cache
from typing import Any

from core.constants import DISCLAIMER
from database.db import init_db
from graph.workflow import compile_graph
from memory.postgres_memory import save_assessment_row
from schemas.assessment import AssessmentResponse


@lru_cache(maxsize=1)
def get_graph():
    init_db()
    return compile_graph()


def run_assessment(
    request: str,
    session_id: str = "default",
    borrower_id: str | None = None,
) -> AssessmentResponse:
    graph = get_graph()
    state: dict[str, Any] = {
        "request": request,
        "session_id": session_id,
        "messages": [{"role": "user", "content": request}],
    }
    if borrower_id:
        state["borrower_id"] = borrower_id
    result = graph.invoke(state)
    response = AssessmentResponse(
        session_id=session_id,
        applicant=result.get("applicant") or {},
        disposition=result.get("disposition"),
        risk_score=result.get("risk_score"),
        probability_of_default=result.get("probability_of_default"),
        recommendations=result.get("recommendations") or [],
        rationale=result.get("rationale"),
        research=_safe_research(result.get("research") or {}),
        analysis=result.get("analysis") or {},
        review=result.get("review") or {},
        plan=result.get("execution_plan") or [],
        disclaimer=DISCLAIMER,
        status="completed",
    )
    save_assessment_row(
        session_id=session_id,
        request=request,
        disposition=response.disposition,
        risk_score=response.risk_score,
        rationale=response.rationale,
        payload_json=response.model_dump_json(),
    )
    return response


def _safe_research(research: dict) -> dict:
    # Keep API payload compact.
    return {
        "query": research.get("query"),
        "products": research.get("products") or [],
        "policy_hits": research.get("policy_hits") or [],
        "web": research.get("web") or [],
        "documents": [
            {"id": hit.get("id"), "metadata": hit.get("metadata"), "text": (hit.get("text") or "")[:400]}
            for hit in (research.get("documents") or [])
        ],
    }


def result_to_dict(response: AssessmentResponse) -> dict:
    return json.loads(response.model_dump_json())
