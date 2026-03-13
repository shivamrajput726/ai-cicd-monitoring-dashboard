from typing import Iterable

import numpy as np
from sklearn.ensemble import IsolationForest
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

    durations = np.array([[r.duration_seconds] for r in runs])
    model = IsolationForest(contamination=0.1, random_state=42)
    model.fit(durations)
    scores = model.decision_function(durations)
    predictions = model.predict(durations)

    result: list[AnomalyScore] = []
    for run, score, pred in zip(runs, scores, predictions, strict=False):
        result.append(
            AnomalyScore(
                run_id=run.id,
                score=float(score),
                is_anomaly=pred == -1,
            )
        )
    return result

