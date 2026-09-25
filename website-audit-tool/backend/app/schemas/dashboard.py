"""
==========================================================
Dashboard Schemas
AI Website Audit Tool
==========================================================

Response schemas used by the dashboard APIs.

These schemas describe the real data returned by:
- /api/dashboard/summary
- /api/dashboard/charts
- /api/dashboard/recent-audits
- /api/dashboard/activity
- /api/dashboard/kpis
- /api/dashboard/trends
==========================================================
"""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


# ==========================================================
# LAST AUDIT
# ==========================================================

class DashboardLastAudit(BaseModel):
    """
    Information about the user's latest audit.
    """

    id: int

    url: str

    created_at: datetime | None = None


# ==========================================================
# DASHBOARD SUMMARY
# ==========================================================

class DashboardSummary(BaseModel):
    """
    Main dashboard summary statistics.
    """

    total_audits: int = 0

    average_score: float = 0

    average_seo: float = 0

    average_performance: float = 0

    average_accessibility: float = 0

    average_security: float = 0

    average_mobile: float = 0

    last_audit: DashboardLastAudit | None = None


# ==========================================================
# DASHBOARD CHART DATASETS
# ==========================================================

class DashboardChartDatasets(BaseModel):
    """
    Score datasets used by the Score Performance chart.
    """

    overall: list[float] = Field(
        default_factory=list
    )

    seo: list[float] = Field(
        default_factory=list
    )

    performance: list[float] = Field(
        default_factory=list
    )

    accessibility: list[float] = Field(
        default_factory=list
    )

    security: list[float] = Field(
        default_factory=list
    )

    mobile: list[float] = Field(
        default_factory=list
    )


# ==========================================================
# DASHBOARD CHARTS
# ==========================================================

class DashboardCharts(BaseModel):
    """
    Data required to render the dashboard
    Score Performance chart.
    """

    period: str

    labels: list[str] = Field(
        default_factory=list
    )

    datasets: DashboardChartDatasets

    count: int = 0


# ==========================================================
# RECENT AUDIT
# ==========================================================

class DashboardRecentAudit(BaseModel):
    """
    Single audit displayed in the Recent Website Audits table.
    """

    id: int

    website_url: str

    overall_score: float = 0

    seo_score: float = 0

    performance_score: float = 0

    accessibility_score: float = 0

    security_score: float = 0

    mobile_score: float = 0

    grade: str = "F"

    created_at: datetime | None = None


# ==========================================================
# PAGINATION
# ==========================================================

class DashboardPagination(BaseModel):
    """
    Pagination information for recent audits.
    """

    page: int

    limit: int

    total: int

    pages: int

    has_next: bool

    has_previous: bool


# ==========================================================
# RECENT AUDITS RESPONSE
# ==========================================================

class DashboardRecentAudits(BaseModel):
    """
    Paginated recent audit response.
    """

    items: list[DashboardRecentAudit] = Field(
        default_factory=list
    )

    pagination: DashboardPagination


# ==========================================================
# DASHBOARD ACTIVITY
# ==========================================================

class DashboardActivityItem(BaseModel):
    """
    Single dashboard activity item.
    """

    id: int

    type: str

    title: str

    description: str

    website_url: str

    overall_score: float = 0

    grade: str = "F"

    created_at: datetime | None = None


# ==========================================================
# GRADE DISTRIBUTION
# ==========================================================

class DashboardGradeDistribution(BaseModel):
    """
    Number of audits in each grade category.
    """

    A: int = 0

    B: int = 0

    C: int = 0

    D: int = 0

    F: int = 0


# ==========================================================
# DASHBOARD KPIs
# ==========================================================

class DashboardKPIs(BaseModel):
    """
    Dashboard KPI statistics.
    """

    total_audits: int = 0

    overall_score: float = 0

    seo_score: float = 0

    performance_score: float = 0

    accessibility_score: float = 0

    security_score: float = 0

    mobile_score: float = 0

    grade_distribution: DashboardGradeDistribution


# ==========================================================
# DASHBOARD TREND ITEM
# ==========================================================

class DashboardTrendItem(BaseModel):
    """
    Single point in the dashboard score trend.
    """

    date: str | None = None

    overall_score: float = 0

    seo_score: float = 0

    performance_score: float = 0

    accessibility_score: float = 0

    security_score: float = 0

    mobile_score: float = 0

    grade: str = "F"

    change: float = 0


# ==========================================================
# DASHBOARD TRENDS
# ==========================================================

class DashboardTrends(BaseModel):
    """
    Dashboard historical trend response.
    """

    period: str

    count: int = 0

    trends: list[DashboardTrendItem] = Field(
        default_factory=list
    )