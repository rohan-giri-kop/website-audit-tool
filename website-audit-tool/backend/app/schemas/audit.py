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

    status: str
    error_message: str | None = None
    duration_seconds: float | None = None

    screenshot_path: str | None = None

    seo_score: float | None = None
    performance_score: float | None = None
    accessibility_score: float | None = None
    security_score: float | None = None
    mobile_score: float | None = None
    uiux_score: float | None = None
    overall_score: float | None = None

    grade: str | None = None
    summary: str | None = None

    seo_metrics: dict[str, Any] | None = None
    performance_metrics: dict[str, Any] | None = None
    accessibility_metrics: dict[str, Any] | None = None
    security_metrics: dict[str, Any] | None = None
    mobile_metrics: dict[str, Any] | None = None
    uiux_metrics: dict[str, Any] | None = None

    page_details: dict[str, Any] | None = None

    recommendations: list[dict[str, Any]] | None = None

    created_at: datetime
    completed_at: datetime | None = None

    findings: list[FindingRead] = []

    model_config = ConfigDict(
        from_attributes=True
    )