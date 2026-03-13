from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.db import get_db
from app.models import RunStatus
from app.schemas import PipelineRunCreate
from app.services import pipeline_service


router = APIRouter(prefix="/events", tags=["events"])


@router.post("/github")
def ingest_github_event(
    payload: dict,
    db: Session = Depends(get_db),
    _: str = Depends(get_current_user),
):
    repository = payload.get("repository", {})
    repo_name = repository.get("full_name")
    branch = payload.get("ref", "").replace("refs/heads/", "")
    workflow_run = payload.get("workflow_run", {})

    pipeline = None
    if repo_name:
        from app.models import Pipeline

        pipeline = (
            db.query(Pipeline)
            .filter(Pipeline.repo == repo_name)
            .filter(Pipeline.branch == branch or Pipeline.branch.is_(None))
            .first()
        )

    if not pipeline:
        return {"detail": "No matching pipeline configured, ignoring"}

    status_str = workflow_run.get("conclusion") or workflow_run.get("status") or "failed"
    status_map = {
        "success": RunStatus.SUCCESS,
        "completed": RunStatus.SUCCESS,
        "failure": RunStatus.FAILED,
        "failed": RunStatus.FAILED,
        "cancelled": RunStatus.CANCELLED,
        "in_progress": RunStatus.RUNNING,
    }
    status = status_map.get(status_str, RunStatus.FAILED)

    run_in = PipelineRunCreate(
        pipeline_id=pipeline.id,
        status=status,
        external_run_id=str(workflow_run.get("id") or ""),
        triggered_by=workflow_run.get("actor", {}).get("login"),
        commit_sha=workflow_run.get("head_sha"),
        branch=branch,
        raw_payload=str(payload),
    )
    pipeline_service.create_pipeline_run(db, run_in)
    return {"detail": "Event ingested"}

