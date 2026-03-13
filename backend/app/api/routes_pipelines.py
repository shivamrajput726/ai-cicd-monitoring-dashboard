from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.db import get_db
from app.models import Pipeline
from app.schemas import PipelineCreate, PipelineRead, PipelineRunCreate, PipelineRunRead, MetricsSummary
from app.services import pipeline_service


router = APIRouter(prefix="/pipelines", tags=["pipelines"])


@router.post("/", response_model=PipelineRead, status_code=status.HTTP_201_CREATED)
def create_pipeline(
    pipeline_in: PipelineCreate,
    db: Session = Depends(get_db),
    _: str = Depends(get_current_user),
) -> PipelineRead:
    pipeline = pipeline_service.create_pipeline(db, pipeline_in)
    return pipeline


@router.get("/", response_model=List[PipelineRead])
def list_pipelines(
    db: Session = Depends(get_db),
    _: str = Depends(get_current_user),
) -> list[PipelineRead]:
    pipelines = pipeline_service.list_pipelines(db)
    return list(pipelines)


@router.get("/{pipeline_id}", response_model=PipelineRead)
def get_pipeline(
    pipeline_id: int,
    db: Session = Depends(get_db),
    _: str = Depends(get_current_user),
) -> PipelineRead:
    pipeline: Pipeline | None = pipeline_service.get_pipeline(db, pipeline_id)
    if pipeline is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pipeline not found")
    return pipeline


@router.post("/{pipeline_id}/runs", response_model=PipelineRunRead, status_code=status.HTTP_201_CREATED)
def create_run(
    pipeline_id: int,
    run_in: PipelineRunCreate,
    db: Session = Depends(get_db),
    _: str = Depends(get_current_user),
) -> PipelineRunRead:
    if run_in.pipeline_id != pipeline_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="pipeline_id mismatch")
    run = pipeline_service.create_pipeline_run(db, run_in)
    return run


@router.get("/{pipeline_id}/runs", response_model=List[PipelineRunRead])
def list_runs(
    pipeline_id: int,
    db: Session = Depends(get_db),
    _: str = Depends(get_current_user),
) -> list[PipelineRunRead]:
    runs = pipeline_service.list_pipeline_runs(db, pipeline_id=pipeline_id)
    return runs


@router.get("/{pipeline_id}/metrics", response_model=MetricsSummary)
def pipeline_metrics(
    pipeline_id: int,
    db: Session = Depends(get_db),
    _: str = Depends(get_current_user),
) -> MetricsSummary:
    total_runs, success_rate, avg_duration = pipeline_service.compute_basic_metrics(db, pipeline_id=pipeline_id)
    return MetricsSummary(
        total_runs=total_runs,
        success_rate=success_rate,
        average_duration_seconds=avg_duration,
    )

