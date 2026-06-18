from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from backend.app.models.audit import Audit
from backend.app.models.finding import Finding
from backend.app.schemas.audit import AuditRequest
from backend.app.utils.audit_analyzer import analyze_website
from backend.app.analyzers.uiux_analyzer import analyze_uiux
from backend.app.utils.screenshot import capture_screenshot


def create_audit(db: Session, user_id: int, request: AuditRequest) -> Audit:
    analysis = analyze_website(str(request.website_url))
    audit = Audit(
        user_id=user_id,
        website_url=str(request.website_url),

        seo_score=analysis["seo_score"],
        performance_score=analysis["performance_score"],
        
        screenshot_path=analysis.get("screenshot_path"),

        accessibility_score=analysis["accessibility_score"],
        accessibility_metrics=analysis.get(
            "accessibility_metrics",
            {}
        ),

        security_score=analysis["security_score"],
        security_metrics=analysis.get(
            "security_metrics",
            {}
        ),

        mobile_score=analysis["mobile_score"],
        mobile_metrics=analysis.get(
            "mobile_metrics",
            {}
        ),

        overall_score=analysis["overall_score"],
        summary=analysis["summary"],
        
        recommendations=(
            analysis.get("recommendations", [])
            if isinstance(
                analysis.get("recommendations", []),
                list
            )
            else []
        ),           
             
        grade=analysis["grade"],
    )  
      
    db.add(audit)
    db.flush()

    for item in analysis["findings"]:
        db.add(
            Finding(
                audit_id=audit.id,
                category=item["category"],

                title=item["issue"],
                severity=item["priority"],
                description=item["issue"],

                issue=item["issue"],
                recommendation=item["recommendation"],
                priority=item["priority"],
                benefit=item["benefit"],
            )       
        )
        
    db.commit()
    db.refresh(audit)
    return audit


def list_audits(db: Session, user_id: int) -> list[Audit]:
    return list(db.execute(select(Audit).where(Audit.user_id == user_id).order_by(desc(Audit.created_at))).scalars().all())


def get_audit(db: Session, audit_id: int, user_id: int) -> Audit | None:
    return db.execute(select(Audit).where(Audit.id == audit_id, Audit.user_id == user_id)).scalar_one_or_none()


def dashboard_summary(db: Session, user_id: int) -> dict:
    audits = list_audits(db, user_id)
    if not audits:
        return {
            "total_audits": 0,
            "average_score": 0,
            "seo_score": 0,
            "performance_score": 0,
            "accessibility_score": 0,
            "security_score": 0,
            "mobile_score": 0,
        }

    total = len(audits)
    return {
        "total_audits": total,
        "average_score": round(sum(a.overall_score for a in audits) / total, 1),
        "seo_score": round(sum(a.seo_score for a in audits) / total, 1),
        "performance_score": round(sum(a.performance_score for a in audits) / total, 1),
        "accessibility_score": round(sum(a.accessibility_score for a in audits) / total, 1),
        "security_score": round(sum(a.security_score for a in audits) / total, 1),
        "mobile_score": round(sum(a.mobile_score for a in audits) / total, 1),
    }
