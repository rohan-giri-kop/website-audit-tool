"""
==========================================================
Dashboard Service
AI Website Audit Tool
==========================================================

Responsibilities:
- Read real audit data
- Calculate dashboard averages
- Build chart datasets
- Return recent audits
- Build dashboard activity
- Calculate KPI statistics
- Build score trends

This file contains dashboard BUSINESS LOGIC.

API routes belong in:

backend/app/api/dashboard.py
==========================================================
"""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any

from sqlalchemy.orm import Session

from backend.app.models.audit import Audit


# ==========================================================
# CONSTANTS
# ==========================================================

DEFAULT_PAGE = 1

DEFAULT_LIMIT = 10

MAX_LIMIT = 100

DEFAULT_PERIOD = "30d"


# ==========================================================
# HELPERS
# ==========================================================

def safe_float(value: Any) -> float:
    """
    Convert a value to float safely.
    """

    try:
        return float(value)

    except (
        TypeError,
        ValueError,
    ):
        return 0.0


def safe_int(value: Any) -> int:
    """
    Convert a value to int safely.
    """

    try:
        return int(value)

    except (
        TypeError,
        ValueError,
    ):
        return 0


def safe_datetime(value: Any) -> datetime | None:
    """
    Return datetime value safely.
    """

    if isinstance(value, datetime):
        return value

    return None


def safe_iso_datetime(value: Any) -> str | None:
    """
    Convert datetime to ISO string safely.
    """

    date_value = safe_datetime(value)

    if date_value is None:
        return None

    return date_value.isoformat()


# ==========================================================
# DASHBOARD SERVICE
# ==========================================================

class DashboardService:
    """
    Dashboard business logic service.

    Every query is restricted to the authenticated
    user's user_id.
    """

    def __init__(
        self,
        db: Session,
        user_id: int,
    ):
        self.db = db
        self.user_id = user_id


    # ======================================================
    # BASE USER AUDIT QUERY
    # ======================================================

    def _user_audits_query(self):
        """
        Return the base query containing only
        audits belonging to the current user.
        """

        return (
            self.db.query(Audit)
            .filter(
                Audit.user_id == self.user_id
            )
        )


    # ======================================================
    # DASHBOARD SUMMARY
    # ======================================================

    def get_dashboard_summary(self) -> dict:
        """
        Calculate the main dashboard summary.

        Returns:
        - Total audits
        - Average overall score
        - Average SEO
        - Average performance
        - Average accessibility
        - Average security
        - Average mobile
        - Latest audit
        """

        audits = (
            self._user_audits_query()
            .order_by(
                Audit.created_at.desc()
            )
            .all()
        )

        total_audits = len(audits)


        # --------------------------------------------------
        # EMPTY DASHBOARD
        # --------------------------------------------------

        if total_audits == 0:

            return {
                "total_audits": 0,
                "average_score": 0,
                "average_seo": 0,
                "average_performance": 0,
                "average_accessibility": 0,
                "average_security": 0,
                "average_mobile": 0,
                "last_audit": None,
            }


        # --------------------------------------------------
        # TOTALS
        # --------------------------------------------------

        total_score = 0.0

        total_seo = 0.0

        total_performance = 0.0

        total_accessibility = 0.0

        total_security = 0.0

        total_mobile = 0.0


        for audit in audits:

            total_score += safe_float(
                audit.overall_score
            )

            total_seo += safe_float(
                audit.seo_score
            )

            total_performance += safe_float(
                audit.performance_score
            )

            total_accessibility += safe_float(
                audit.accessibility_score
            )

            total_security += safe_float(
                audit.security_score
            )

            total_mobile += safe_float(
                audit.mobile_score
            )


        # --------------------------------------------------
        # LATEST AUDIT
        # --------------------------------------------------

        latest_audit = audits[0]


        return {
            "total_audits": total_audits,

            "average_score": round(
                total_score / total_audits,
                2,
            ),

            "average_seo": round(
                total_seo / total_audits,
                2,
            ),

            "average_performance": round(
                total_performance / total_audits,
                2,
            ),

            "average_accessibility": round(
                total_accessibility / total_audits,
                2,
            ),

            "average_security": round(
                total_security / total_audits,
                2,
            ),

            "average_mobile": round(
                total_mobile / total_audits,
                2,
            ),

            "last_audit": {
                "id": latest_audit.id,

                "url": latest_audit.website_url,

                "created_at":
                    safe_iso_datetime(
                        latest_audit.created_at
                    ),
            },
        }


    # ======================================================
    # SCORE PERFORMANCE CHART
    # ======================================================

    def get_dashboard_charts(
        self,
        period: str = DEFAULT_PERIOD,
    ) -> dict:
        """
        Build Score Performance chart data.

        Supported periods:
        - 7d
        - 30d
        - 90d
        - 365d
        """

        period_days = {
            "7d": 7,
            "30d": 30,
            "90d": 90,
            "365d": 365,
        }


        if period not in period_days:

            period = DEFAULT_PERIOD


        days = period_days[period]


        start_date = (
            datetime.utcnow()
            - timedelta(days=days)
        )


        audits = (
            self._user_audits_query()
            .filter(
                Audit.created_at >= start_date
            )
            .order_by(
                Audit.created_at.asc()
            )
            .all()
        )


        labels = []

        overall_scores = []

        seo_scores = []

        performance_scores = []

        accessibility_scores = []

        security_scores = []

        mobile_scores = []


        for audit in audits:

            created_at = safe_datetime(
                    audit.created_at
                )


            if created_at:

                labels.append(
                    created_at.strftime(
                        "%d %b"
                    )
                )

            else:

                labels.append("—")


            overall_scores.append(
                safe_float(
                    audit.overall_score
                )
            )

            seo_scores.append(
                safe_float(
                    audit.seo_score
                )
            )

            performance_scores.append(
                safe_float(
                    audit.performance_score
                )
            )

            accessibility_scores.append(
                safe_float(
                    audit.accessibility_score
                )
            )

            security_scores.append(
                safe_float(
                    audit.security_score
                )
            )

            mobile_scores.append(
                safe_float(
                    audit.mobile_score
                )
            )


        return {
            "period": period,

            "labels": labels,

            "count": len(audits),

            "datasets": {
                "overall": overall_scores,

                "seo": seo_scores,

                "performance":
                    performance_scores,

                "accessibility":
                    accessibility_scores,

                "security":
                    security_scores,

                "mobile":
                    mobile_scores,
            },
        }


    # ======================================================
    # RECENT AUDITS
    # ======================================================

    def get_recent_audits(
        self,
        page: int = DEFAULT_PAGE,
        limit: int = DEFAULT_LIMIT,
        search: str | None = None,
    ) -> dict:
        """
        Return paginated recent audits.
        """

        page = max(
            1,
            safe_int(page),
        )

        limit = min(
            MAX_LIMIT,
            max(
                1,
                safe_int(limit),
            ),
        )


        query = (
            self._user_audits_query()
        )


        # --------------------------------------------------
        # SEARCH
        # --------------------------------------------------

        if search:

            search_value = search.strip()

            if search_value:

                query = query.filter(
                    Audit.website_url.ilike(
                        f"%{search_value}%"
                    )
                )


        # --------------------------------------------------
        # TOTAL
        # --------------------------------------------------

        total = query.count()


        # --------------------------------------------------
        # PAGINATED AUDITS
        # --------------------------------------------------

        audits = (
            query
            .order_by(
                Audit.created_at.desc()
            )
            .offset(
                (page - 1) * limit
            )
            .limit(limit)
            .all()
        )


        items = []


        for audit in audits:

            items.append({

                "id":
                    audit.id,

                "website_url":
                    audit.website_url,

                "overall_score":
                    safe_float(
                        audit.overall_score
                    ),

                "seo_score":
                    safe_float(
                        audit.seo_score
                    ),

                "performance_score":
                    safe_float(
                        audit.performance_score
                    ),

                "accessibility_score":
                    safe_float(
                        audit.accessibility_score
                    ),

                "security_score":
                    safe_float(
                        audit.security_score
                    ),

                "mobile_score":
                    safe_float(
                        audit.mobile_score
                    ),

                "grade":
                    (
                        audit.grade or "F"
                    ).upper(),

                "created_at":
                    safe_iso_datetime(
                        audit.created_at
                    ),
            })


        total_pages = (
            (total + limit - 1)
            // limit
        )


        return {
            "items": items,

            "pagination": {
                "page": page,

                "limit": limit,

                "total": total,

                "pages": total_pages,

                "has_next":
                    page < total_pages,

                "has_previous":
                    page > 1,
            },
        }


    # ======================================================
    # DASHBOARD ACTIVITY
    # ======================================================

    def get_dashboard_activity(
        self,
        limit: int = DEFAULT_LIMIT,
    ) -> list[dict]:
        """
        Build dashboard activity from
        recent audit history.
        """

        limit = min(
            MAX_LIMIT,
            max(
                1,
                safe_int(limit),
            ),
        )


        audits = (
            self._user_audits_query()
            .order_by(
                Audit.created_at.desc()
            )
            .limit(limit)
            .all()
        )


        activities = []


        for audit in audits:

            activities.append({

                "id":
                    audit.id,

                "type":
                    "audit",

                "title":
                    "Website Audit Completed",

                "description":
                    (
                        "Audit completed for "
                        f"{audit.website_url}"
                    ),

                "website_url":
                    audit.website_url,

                "overall_score":
                    safe_float(
                        audit.overall_score
                    ),

                "grade":
                    (
                        audit.grade or "F"
                    ).upper(),

                "created_at":
                    safe_iso_datetime(
                        audit.created_at
                    ),
            })


        return activities


    # ======================================================
    # DASHBOARD KPIs
    # ======================================================

    def get_dashboard_kpis(self) -> dict:
        """
        Calculate dashboard KPI metrics.
        """

        audits = (
            self._user_audits_query()
            .all()
        )


        total = len(audits)


        # --------------------------------------------------
        # EMPTY STATE
        # --------------------------------------------------

        if total == 0:

            return {
                "total_audits": 0,

                "overall_score": 0,

                "seo_score": 0,

                "performance_score": 0,

                "accessibility_score": 0,

                "security_score": 0,

                "mobile_score": 0,

                "grade_distribution": {
                    "A": 0,
                    "B": 0,
                    "C": 0,
                    "D": 0,
                    "F": 0,
                },
            }


        # --------------------------------------------------
        # TOTALS
        # --------------------------------------------------

        overall_total = 0.0

        seo_total = 0.0

        performance_total = 0.0

        accessibility_total = 0.0

        security_total = 0.0

        mobile_total = 0.0


        grade_distribution = {
            "A": 0,
            "B": 0,
            "C": 0,
            "D": 0,
            "F": 0,
        }


        for audit in audits:

            overall_total += safe_float(
                audit.overall_score
            )

            seo_total += safe_float(
                audit.seo_score
            )

            performance_total += safe_float(
                audit.performance_score
            )

            accessibility_total += safe_float(
                audit.accessibility_score
            )

            security_total += safe_float(
                audit.security_score
            )

            mobile_total += safe_float(
                audit.mobile_score
            )


            grade = (
                audit.grade or "F"
            ).upper()


            if grade in grade_distribution:

                grade_distribution[grade] += 1

            else:

                grade_distribution["F"] += 1


        return {
            "total_audits": total,

            "overall_score": round(
                overall_total / total,
                2,
            ),

            "seo_score": round(
                seo_total / total,
                2,
            ),

            "performance_score": round(
                performance_total / total,
                2,
            ),

            "accessibility_score": round(
                accessibility_total / total,
                2,
            ),

            "security_score": round(
                security_total / total,
                2,
            ),

            "mobile_score": round(
                mobile_total / total,
                2,
            ),

            "grade_distribution":
                grade_distribution,
        }


    # ======================================================
    # DASHBOARD TRENDS
    # ======================================================

    def get_dashboard_trends(
        self,
        period: str = DEFAULT_PERIOD,
    ) -> dict:
        """
        Build historical score trends.
        """

        period_days = {
            "7d": 7,
            "30d": 30,
            "90d": 90,
            "365d": 365,
        }


        if period not in period_days:

            period = DEFAULT_PERIOD


        days = period_days[period]


        start_date = (
            datetime.utcnow()
            - timedelta(days=days)
        )


        audits = (
            self._user_audits_query()
            .filter(
                Audit.created_at >= start_date
            )
            .order_by(
                Audit.created_at.asc()
            )
            .all()
        )


        trends = []


        previous_score = None


        for audit in audits:

            current_score = safe_float(
                audit.overall_score
            )


            if previous_score is None:

                change = 0

            else:

                change = round(
                    current_score
                    - previous_score,
                    2,
                )


            created_at = safe_datetime(
                    audit.created_at
                )


            date_value = (
                created_at.strftime(
                    "%Y-%m-%d"
                )
                if created_at
                else None
            )


            trends.append({

                "date":
                    date_value,

                "overall_score":
                    current_score,

                "seo_score":
                    safe_float(
                        audit.seo_score
                    ),

                "performance_score":
                    safe_float(
                        audit.performance_score
                    ),

                "accessibility_score":
                    safe_float(
                        audit.accessibility_score
                    ),

                "security_score":
                    safe_float(
                        audit.security_score
                    ),

                "mobile_score":
                    safe_float(
                        audit.mobile_score
                    ),

                "grade":
                    (
                        audit.grade or "F"
                    ).upper(),

                "change":
                    change,
            })


            previous_score = current_score


        return {
            "period": period,

            "count": len(trends),

            "trends": trends,
        }