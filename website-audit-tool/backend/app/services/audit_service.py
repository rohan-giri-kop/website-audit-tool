from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import select, func
from sqlalchemy.orm import Session

from backend.app.models.audit import Audit
from backend.app.models.finding import Finding
from backend.app.utils.audit_analyzer import analyze_website


# ==========================================================
# HELPERS
# ==========================================================

def _safe_float(value):
    """
    Convert a score to float without converting None to 0.

    None means the analyzer did not produce a valid score.
    """

    if value is None:
        return None

    try:
        return round(float(value), 1)
    except (TypeError, ValueError):
        return None


def _safe_dict(value):
    """
    Ensure JSON fields always receive a dictionary.
    """

    if isinstance(value, dict):
        return value

    return {}


def _safe_list(value):
    """
    Ensure list fields always receive a list.
    """

    if isinstance(value, list):
        return value

    return []


def _utc_now():
    return datetime.now(timezone.utc)


# ==========================================================
# CREATE AUDIT
# ==========================================================

def create_audit(
    db: Session,
    user_id: int,
    website_url: str,
):
    """
    Run the complete real website audit and persist
    the result into the database.

    The analyzer is the source of truth for:
        - scores
        - metrics
        - findings
        - recommendations
        - status
        - duration
        - page details
    """

    # ------------------------------------------------------
    # RUN REAL ANALYZER
    # ------------------------------------------------------
    
    
    website_url = str(website_url).strip()

    if not website_url:
        raise ValueError("Website URL is required")

    print(
        f"[AUDIT SERVICE] URL type: {type(website_url).__name__}"
    )

    print(
        f"[AUDIT SERVICE] URL: {website_url}"
    )

    result = analyze_website(
        website_url
    )
    

    if not isinstance(result, dict):
        raise RuntimeError(
            "Audit analyzer returned an invalid result."
        )

    # ------------------------------------------------------
    # EXTRACT RESULT
    # ------------------------------------------------------

    status = result.get(
        "status",
        "completed",
    )

    error_message = result.get(
        "error_message"
    )

    duration_seconds = _safe_float(
        result.get(
            "duration_seconds"
        )
    )

    # ------------------------------------------------------
    # SCORES
    # ------------------------------------------------------

    seo_score = _safe_float(
        result.get(
            "seo_score"
        )
    )

    performance_score = _safe_float(
        result.get(
            "performance_score"
        )
    )

    accessibility_score = _safe_float(
        result.get(
            "accessibility_score"
        )
    )

    security_score = _safe_float(
        result.get(
            "security_score"
        )
    )

    mobile_score = _safe_float(
        result.get(
            "mobile_score"
        )
    )

    uiux_score = _safe_float(
        result.get(
            "uiux_score"
        )
    )

    overall_score = _safe_float(
        result.get(
            "overall_score"
        )
    )

    grade = result.get(
        "grade"
    )

    summary = result.get(
        "summary"
    )

    # ------------------------------------------------------
    # METRICS
    # ------------------------------------------------------

    seo_metrics = _safe_dict(
        result.get(
            "seo_metrics"
        )
    )

    performance_metrics = _safe_dict(
        result.get(
            "performance_metrics"
        )
    )

    accessibility_metrics = _safe_dict(
        result.get(
            "accessibility_metrics"
        )
    )

    security_metrics = _safe_dict(
        result.get(
            "security_metrics"
        )
    )

    mobile_metrics = _safe_dict(
        result.get(
            "mobile_metrics"
        )
    )

    uiux_metrics = _safe_dict(
        result.get(
            "uiux_metrics"
        )
    )

    page_details = _safe_dict(
        result.get(
            "page_details"
        )
    )

    recommendations = _safe_list(
        result.get(
            "recommendations"
        )
    )

    findings = _safe_list(
        result.get(
            "findings"
        )
    )

    screenshot_path = result.get(
        "screenshot_path"
    )

    # ------------------------------------------------------
    # COMPLETION TIME
    # ------------------------------------------------------

    completed_at = None

    if status in (
        "completed",
        "completed_with_errors",
    ):
        completed_at = _utc_now()

    # ------------------------------------------------------
    # CREATE AUDIT
    # ------------------------------------------------------

    audit = Audit(
        user_id=user_id,

        website_url=website_url,

        # Scores
        seo_score=seo_score,
        performance_score=performance_score,
        accessibility_score=accessibility_score,
        security_score=security_score,
        mobile_score=mobile_score,
        uiux_score=uiux_score,
        overall_score=overall_score,

        # Result information
        grade=grade,
        summary=summary,
        recommendations=recommendations,
        screenshot_path=screenshot_path,

        # Audit execution state
        status=status,
        error_message=error_message,
        duration_seconds=duration_seconds,
        completed_at=completed_at,

        # REAL analyzer metrics
        seo_metrics=seo_metrics,
        performance_metrics=performance_metrics,
        accessibility_metrics=accessibility_metrics,
        security_metrics=security_metrics,
        mobile_metrics=mobile_metrics,
        uiux_metrics=uiux_metrics,

        # Page information
        page_details=page_details,
    )
    
    db.add(audit)

    # Flush first so audit.id exists
    # before creating Finding rows.
    db.flush()

    # ------------------------------------------------------
    # SAVE FINDINGS
    # ------------------------------------------------------

    for item in findings:

        if not isinstance(item, dict):
            continue

        # -----------------------------------------------
        # BASIC FINDING DATA
        # -----------------------------------------------

        category = str(
            item.get(
                "category",
                "General"
            )
        )

        issue = str(
            item.get(
                "issue",
                item.get(
                    "title",
                    "Issue detected."
                )
            )
        )

        recommendation = str(
            item.get(
                "recommendation",
                "Review this issue."
            )
        )

        priority = str(
            item.get(
                "priority",
                item.get(
                    "severity",
                    "Medium"
                )
            )
        )

        benefit = str(
            item.get(
                "benefit",
                "Improves website quality."
            )
        )

        # -----------------------------------------------
        # DATABASE REQUIRED FIELDS
        # -----------------------------------------------

        title = str(
            item.get(
                "title",
                issue
            )
        )

        severity = str(
            item.get(
                "severity",
                priority
            )
        )

        description = str(
            item.get(
                "description",
                issue
            )
        )

        # -----------------------------------------------
        # CREATE FINDING
        # -----------------------------------------------

        finding = Finding(
            audit_id=audit.id,

            category=category,

            # Required legacy/report fields
            title=title,
            severity=severity,
            description=description,

            # Current structured fields
            issue=issue,
            recommendation=recommendation,
            priority=priority,
            benefit=benefit,
        )

        db.add(finding)
        
        # ------------------------------------------------------
        # COMMIT
        # ------------------------------------------------------

        db.commit()

        db.refresh(audit)

    return audit
    
# ==========================================================
# GET AUDIT
# ==========================================================

def get_audit(
    db: Session,
    audit_id: int,
    user_id: int | None = None,
):
    """
    Return a single audit.

    If user_id is supplied, the audit must belong
    to that user.
    """

    stmt = select(Audit).where(
        Audit.id == audit_id
    )

    if user_id is not None:

        stmt = stmt.where(
            Audit.user_id == user_id
        )

    return db.execute(
        stmt
    ).scalar_one_or_none()


# ==========================================================
# LIST AUDITS
# ==========================================================

def list_audits(
    db: Session,
    user_id: int,
    limit: int = 50,
):
    """
    Return the user's most recent audits.
    """

    limit = max(
        1,
        min(
            int(limit),
            100,
        ),
    )

    stmt = (
        select(Audit)
        .where(
            Audit.user_id == user_id
        )
        .order_by(
            Audit.created_at.desc()
        )
        .limit(limit)
    )

    return db.execute(
        stmt
    ).scalars().all()


# ==========================================================
# GET FINDINGS
# ==========================================================

def get_audit_findings(
    db: Session,
    audit_id: int,
    user_id: int | None = None,
):
    """
    Return findings belonging to an audit.
    """

    # First verify ownership if required.
    if user_id is not None:

        audit = get_audit(
            db,
            audit_id,
            user_id,
        )

        if audit is None:
            return []

    stmt = (
        select(Finding)
        .where(
            Finding.audit_id == audit_id
        )
        .order_by(
            Finding.id.asc()
        )
    )

    return db.execute(
        stmt
    ).scalars().all()


# ==========================================================
# DELETE AUDIT
# ==========================================================

def delete_audit(
    db: Session,
    audit_id: int,
    user_id: int,
):
    """
    Permanently delete an audit and its findings.

    Findings are explicitly removed first so this works
    even when SQLite foreign-key cascade behavior is not
    enabled.
    """

    audit = get_audit(
        db,
        audit_id,
        user_id,
    )

    if audit is None:
        return False

    db.query(Finding).filter(
        Finding.audit_id == audit.id
    ).delete(
        synchronize_session=False
    )

    db.delete(audit)

    db.commit()

    return True


# ==========================================================
# DASHBOARD SUMMARY
# ==========================================================

def dashboard_summary(
    db: Session,
    user_id: int,
):
    """
    Return real database-driven dashboard statistics.

    No fake/demo numbers are generated here.
    """

    # ------------------------------------------------------
    # TOTAL AUDITS
    # ------------------------------------------------------

    total_audits = db.execute(
        select(
            func.count(Audit.id)
        ).where(
            Audit.user_id == user_id
        )
    ).scalar_one()

    # ------------------------------------------------------
    # COMPLETED AUDITS
    # ------------------------------------------------------

    completed_audits = db.execute(
        select(
            func.count(Audit.id)
        ).where(
            Audit.user_id == user_id,
            Audit.status.in_(
                [
                    "completed",
                    "completed_with_errors",
                ]
            ),
        )
    ).scalar_one()

    # ------------------------------------------------------
    # FAILED AUDITS
    # ------------------------------------------------------

    failed_audits = db.execute(
        select(
            func.count(Audit.id)
        ).where(
            Audit.user_id == user_id,
            Audit.status == "failed",
        )
    ).scalar_one()

    # ------------------------------------------------------
    # AVERAGE OVERALL SCORE
    # ------------------------------------------------------

    average_score = db.execute(
        select(
            func.avg(
                Audit.overall_score
            )
        ).where(
            Audit.user_id == user_id,
            Audit.overall_score.is_not(None),
        )
    ).scalar_one()

    if average_score is not None:

        average_score = round(
            float(average_score),
            1,
        )

    # ------------------------------------------------------
    # LATEST AUDIT
    # ------------------------------------------------------

    latest_audit = db.execute(
        select(Audit)
        .where(
            Audit.user_id == user_id
        )
        .order_by(
            Audit.created_at.desc()
        )
        .limit(1)
    ).scalar_one_or_none()

    # ------------------------------------------------------
    # RETURN REAL DATA
    # ------------------------------------------------------

    return {
        "total_audits":
            int(total_audits or 0),

        "completed_audits":
            int(completed_audits or 0),

        "failed_audits":
            int(failed_audits or 0),

        "average_score":
            average_score,

        "latest_audit":
            latest_audit,
    }