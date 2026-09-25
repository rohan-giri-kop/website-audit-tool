"""
==========================================================
Dashboard API
AI Website Audit Tool
==========================================================

Responsibilities:
- Dashboard summary
- Dashboard charts
- Recent audits
- Dashboard activity
- Dashboard KPIs
- Dashboard trends
- Dashboard statistics
- Dashboard health

Business logic is handled by:

backend.app.services.dashboard_service.DashboardService

This file contains API routes only.
==========================================================
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.database.session import get_db
from backend.app.api.auth import get_current_user
from backend.app.models.user import User

from backend.app.services.dashboard_service import (
    DashboardService,
)


# ==========================================================
# ROUTER
# ==========================================================

router = APIRouter(
    prefix="/api/dashboard",
    tags=["Dashboard"],
)


# ==========================================================
# CONSTANTS
# ==========================================================

DEFAULT_PAGE = 1
DEFAULT_LIMIT = 10
MAX_LIMIT = 100
DEFAULT_PERIOD = "30d"


ALLOWED_PERIODS = {
    "7d",
    "30d",
    "90d",
    "365d",
}


# ==========================================================
# STANDARD RESPONSE
# ==========================================================

def success_response(
    data: Any,
    message: str = "Success",
) -> dict:
    """
    Standard dashboard API response.
    """

    return {
        "success": True,
        "message": message,
        "timestamp": datetime.utcnow().isoformat(),
        "data": data,
    }


# ==========================================================
# DASHBOARD SERVICE DEPENDENCY
# ==========================================================

def get_dashboard_service(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> DashboardService:
    """
    Create DashboardService for the authenticated user.
    """

    return DashboardService(
        db=db,
        user_id=current_user.id,
    )


# ==========================================================
# VALIDATION HELPERS
# ==========================================================

def validate_period(
    period: str,
) -> str:
    """
    Validate dashboard period.
    """

    if period not in ALLOWED_PERIODS:
        return DEFAULT_PERIOD

    return period


def validate_page(
    page: int,
) -> int:
    """
    Validate pagination page.
    """

    try:
        page = int(page)
    except (
        TypeError,
        ValueError,
    ):
        return DEFAULT_PAGE

    return max(
        DEFAULT_PAGE,
        page,
    )


def validate_limit(
    limit: int,
) -> int:
    """
    Validate pagination limit.
    """

    try:
        limit = int(limit)
    except (
        TypeError,
        ValueError,
    ):
        return DEFAULT_LIMIT

    return min(
        MAX_LIMIT,
        max(
            1,
            limit,
        ),
    )


# ==========================================================
# DASHBOARD SUMMARY
# ==========================================================

@router.get("/summary")
def get_dashboard_summary(
    service: DashboardService = Depends(
        get_dashboard_service
    ),
):
    """
    Return the main dashboard summary.

    Includes:
    - Total audits
    - Average overall score
    - Average SEO score
    - Average performance score
    - Average accessibility score
    - Average security score
    - Average mobile score
    - Latest audit
    """

    try:

        summary = (
            service.get_dashboard_summary()
        )

        return success_response(
            data=summary,
            message="Dashboard summary loaded.",
        )

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=(
                "Unable to load dashboard summary."
            ),
        ) from exc


# ==========================================================
# DASHBOARD CHARTS
# ==========================================================

@router.get("/charts")
def get_dashboard_charts(
    period: str = DEFAULT_PERIOD,
    service: DashboardService = Depends(
        get_dashboard_service
    ),
):
    """
    Return Score Performance chart data.

    Supported periods:
    - 7d
    - 30d
    - 90d
    - 365d
    """

    period = validate_period(
        period
    )

    try:

        charts = (
            service.get_dashboard_charts(
                period=period
            )
        )

        return success_response(
            data=charts,
            message="Dashboard charts loaded.",
        )

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=(
                "Unable to load dashboard charts."
            ),
        ) from exc


# ==========================================================
# RECENT AUDITS
# ==========================================================

@router.get("/recent-audits")
def get_recent_audits(
    page: int = DEFAULT_PAGE,
    limit: int = DEFAULT_LIMIT,
    search: str | None = None,
    service: DashboardService = Depends(
        get_dashboard_service
    ),
):
    """
    Return paginated recent audits belonging
    to the authenticated user.
    """

    page = validate_page(
        page
    )

    limit = validate_limit(
        limit
    )

    try:

        audits = (
            service.get_recent_audits(
                page=page,
                limit=limit,
                search=search,
            )
        )

        return success_response(
            data=audits,
            message="Recent audits loaded.",
        )

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=(
                "Unable to load recent audits."
            ),
        ) from exc


# ==========================================================
# DASHBOARD ACTIVITY
# ==========================================================

@router.get("/activity")
def get_dashboard_activity(
    limit: int = DEFAULT_LIMIT,
    service: DashboardService = Depends(
        get_dashboard_service
    ),
):
    """
    Return recent dashboard activity.
    """

    limit = validate_limit(
        limit
    )

    try:

        activity = (
            service.get_dashboard_activity(
                limit=limit
            )
        )

        return success_response(
            data=activity,
            message="Dashboard activity loaded.",
        )

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=(
                "Unable to load dashboard activity."
            ),
        ) from exc


# ==========================================================
# DASHBOARD KPIs
# ==========================================================

@router.get("/kpis")
def get_dashboard_kpis(
    service: DashboardService = Depends(
        get_dashboard_service
    ),
):
    """
    Return dashboard KPI metrics.

    Includes:
    - Overall score
    - SEO score
    - Performance score
    - Accessibility score
    - Security score
    - Mobile score
    - Grade distribution
    """

    try:

        kpis = (
            service.get_dashboard_kpis()
        )

        return success_response(
            data=kpis,
            message="Dashboard KPIs loaded.",
        )

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=(
                "Unable to load dashboard KPIs."
            ),
        ) from exc


# ==========================================================
# DASHBOARD TRENDS
# ==========================================================

@router.get("/trends")
def get_dashboard_trends(
    period: str = DEFAULT_PERIOD,
    service: DashboardService = Depends(
        get_dashboard_service
    ),
):
    """
    Return historical score trends.
    """

    period = validate_period(
        period
    )

    try:

        trends = (
            service.get_dashboard_trends(
                period=period
            )
        )

        return success_response(
            data=trends,
            message="Dashboard trends loaded.",
        )

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=(
                "Unable to load dashboard trends."
            ),
        ) from exc


# ==========================================================
# DASHBOARD STATISTICS
# ==========================================================

@router.get("/statistics")
def dashboard_statistics(
    service: DashboardService = Depends(
        get_dashboard_service
    ),
):
    """
    Return combined dashboard statistics.
    """

    try:

        statistics = {

            "summary":
                service.get_dashboard_summary(),

            "kpis":
                service.get_dashboard_kpis(),

            "activity":
                service.get_dashboard_activity(
                    limit=5
                ),

        }

        return success_response(
            data=statistics,
            message="Dashboard statistics loaded.",
        )

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=(
                "Unable to load dashboard statistics."
            ),
        ) from exc


# ==========================================================
# DASHBOARD HEALTH
# ==========================================================

@router.get("/health")
def dashboard_health():
    """
    Dashboard API health check.
    """

    return {
        "success": True,
        "service": "dashboard",
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
    }


# ==========================================================
# DASHBOARD API INFORMATION
# ==========================================================

@router.get("")
def dashboard_info():
    """
    Return available dashboard API routes.
    """

    return {
        "success": True,
        "service": "Dashboard API",
        "version": "3.0.0",
        "available_routes": [
            "/summary",
            "/charts",
            "/recent-audits",
            "/activity",
            "/kpis",
            "/trends",
            "/statistics",
            "/health",
        ],
    }