from datetime import datetime
from typing import Iterable

from sqlalchemy.orm import Session

from app.models import Pipeline, PipelineRun, RunStatus
from app.schemas import PipelineCreate, PipelineRunCreate


def create_pipeline(db: Session, pipeline_in: PipelineCreate) -> Pipeline:
    pipeline = Pipeline(
        name=pipeline_in.name,
        provider=pipeline_in.provider,
        repo=pipeline_in.repo,
        branch=pipeline_in.branch,
    )
    db.add(pipeline)
    db.commit()
    db.refresh(pipeline)
    return pipeline


def list_pipelines(db: Session) -> Iterable[Pipeline]:
    return db.query(Pipeline).order_by(Pipeline.created_at.desc()).all()


def get_pipeline(db: Session, pipeline_id: int) -> Pipeline | None:
    return db.query(Pipeline).filter(Pipeline.id == pipeline_id).first()


def create_pipeline_run(db: Session, run_in: PipelineRunCreate) -> PipelineRun:
    started_at = run_in.started_at or datetime.utcnow()
    duration_seconds = run_in.duration_seconds
    finished_at = run_in.finished_at
    if finished_at and not duration_seconds:
        duration_seconds = (finished_at - started_at).total_seconds()

    run = PipelineRun(
        pipeline_id=run_in.pipeline_id,
        external_run_id=run_in.external_run_id,
        status=run_in.status,
        started_at=started_at,
        finished_at=finished_at,
        duration_seconds=duration_seconds,
        triggered_by=run_in.triggered_by,
        commit_sha=run_in.commit_sha,
        branch=run_in.branch,
        raw_payload=run_in.raw_payload,
    )
    db.add(run)
    db.commit()
    db.refresh(run)
    return run


def list_pipeline_runs(db: Session, pipeline_id: int, limit: int = 50) -> list[PipelineRun]:
    return (
        db.query(PipelineRun)
        .filter(PipelineRun.pipeline_id == pipeline_id)
        .order_by(PipelineRun.started_at.desc())
        .limit(limit)
        .all()
    )


def compute_basic_metrics(db: Session, pipeline_id: int | None = None):
    query = db.query(PipelineRun)
    if pipeline_id is not None:
        query = query.filter(PipelineRun.pipeline_id == pipeline_id)

    runs = query.all()
    total_runs = len(runs)
    if total_runs == 0:
        return 0, 0.0, None

    success_count = sum(1 for r in runs if r.status == RunStatus.SUCCESS)
    durations = [r.duration_seconds for r in runs if r.duration_seconds is not None]
    average_duration = sum(durations) / len(durations) if durations else None
    success_rate = success_count / total_runs if total_runs else 0.0
    return total_runs, success_rate, average_duration

