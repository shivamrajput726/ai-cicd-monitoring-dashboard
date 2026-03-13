from datetime import datetime
from enum import Enum
from typing import Optional, List

from pydantic import BaseModel, EmailStr

from app.models import UserRole, RunStatus


class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: str
    role: UserRole = UserRole.VIEWER


class UserRead(UserBase):
    id: int
    is_active: bool
    role: UserRole
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: str
    exp: int


class PipelineBase(BaseModel):
    name: str
    provider: Optional[str] = None
    repo: Optional[str] = None
    branch: Optional[str] = None


class PipelineCreate(PipelineBase):
    pass


class PipelineRead(PipelineBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class PipelineRunBase(BaseModel):
    status: RunStatus
    external_run_id: Optional[str] = None
    triggered_by: Optional[str] = None
    commit_sha: Optional[str] = None
    branch: Optional[str] = None


class PipelineRunCreate(PipelineRunBase):
    pipeline_id: int
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    duration_seconds: Optional[float] = None
    raw_payload: Optional[str] = None


class PipelineRunRead(PipelineRunBase):
    id: int
    pipeline_id: int
    started_at: datetime
    finished_at: Optional[datetime] = None
    duration_seconds: Optional[float] = None

    class Config:
        from_attributes = True


class RunMetricRead(BaseModel):
    id: int
    run_id: int
    name: str
    value: float
    created_at: datetime

    class Config:
        from_attributes = True


class AnomalyScore(BaseModel):
    run_id: int
    score: float
    is_anomaly: bool


class MetricsSummary(BaseModel):
    total_runs: int
    success_rate: float
    average_duration_seconds: Optional[float]

