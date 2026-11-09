from graph.pipeline import result_to_dict, run_assessment
from worker.celery_app import celery_app


@celery_app.task(name="worker.tasks.assess_task")
def assess_task(request: str, session_id: str, borrower_id: str | None = None) -> dict:
    response = run_assessment(request, session_id=session_id, borrower_id=borrower_id)
    return result_to_dict(response)
