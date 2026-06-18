from pydantic import BaseModel


class DashboardSummary(BaseModel):
    total_audits: int
    average_score: float
    seo_score: float
    performance_score: float
    accessibility_score: float
    security_score: float
    mobile_score: float
