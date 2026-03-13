from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.db import get_db
from app.schemas import AnomalyScore, MetricsSummary
from app.services import anomaly_service, pipeline_service


router = APIRouter(prefix="/insights", tags=["insights"])


@router.get("/anomalies", response_model=List[AnomalyScore])
def list_anomalies(
    pipeline_id: int | None = None,
    db: Session = Depends(get_db),
    _: str = Depends(get_current_user),
) -> list[AnomalyScore]:
    return anomaly_service.compute_anomaly_scores(db, pipeline_id=pipeline_id)


@router.get("/metrics/summary", response_model=MetricsSummary)
def global_metrics(
    db: Session = Depends(get_db),
    _: str = Depends(get_current_user),
) -> MetricsSummary:
    total_runs, success_rate, avg_duration = pipeline_service.compute_basic_metrics(db, pipeline_id=None)
    return MetricsSummary(
        total_runs=total_runs,
        success_rate=success_rate,
        average_duration_seconds=avg_duration,
    )

