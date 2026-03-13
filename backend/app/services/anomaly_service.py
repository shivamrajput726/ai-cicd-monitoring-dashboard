from __future__ import annotations

from typing import Iterable

import math
from sqlalchemy.orm import Session

from app.models import PipelineRun
from app.schemas import AnomalyScore


def compute_anomaly_scores(db: Session, pipeline_id: int | None = None) -> list[AnomalyScore]:
    query = db.query(PipelineRun)
    if pipeline_id is not None:
        query = query.filter(PipelineRun.pipeline_id == pipeline_id)

    runs: Iterable[PipelineRun] = query.order_by(PipelineRun.started_at.asc()).all()
    runs = [r for r in runs if r.duration_seconds is not None]

    if not runs:
        return []

    durations = [float(r.duration_seconds) for r in runs if r.duration_seconds is not None]
    if len(durations) < 5:
        # Not enough history to score anomalies robustly
        return [AnomalyScore(run_id=r.id, score=0.0, is_anomaly=False) for r in runs]

    mean = sum(durations) / len(durations)
    variance = sum((d - mean) ** 2 for d in durations) / (len(durations) - 1)
    std = math.sqrt(variance) if variance > 0 else 0.0

    result: list[AnomalyScore] = []
    for run in runs:
        d = float(run.duration_seconds or 0.0)
        z = (d - mean) / std if std > 0 else 0.0
        # Simple statistical rule: |z| >= 2.5 flags anomaly
        is_anomaly = abs(z) >= 2.5
        result.append(
            AnomalyScore(
                run_id=run.id,
                score=float(z),
                is_anomaly=is_anomaly,
            )
        )
    return result

