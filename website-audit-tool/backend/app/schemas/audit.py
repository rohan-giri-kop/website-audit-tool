from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field, HttpUrl, ConfigDict
from backend.app.schemas.finding import FindingRead


class AuditRequest(BaseModel):
    website_url: HttpUrl


class AuditRead(BaseModel):
    id: int
    user_id: int
    website_url: str

    screenshot_path: str | None = None

    seo_score: float
    performance_score: float
    accessibility_score: float
    security_score: float
    mobile_score: float
    overall_score: float

    summary: str
    grade: str
    created_at: datetime

    accessibility_metrics: dict[str, Any] | None = None
    security_metrics: dict[str, Any] | None = None
    mobile_metrics: dict[str, Any] | None = None

    recommendations: list[dict[str, Any]] | None = None

    findings: list[FindingRead] = []
    
    model_config = ConfigDict(from_attributes=True)