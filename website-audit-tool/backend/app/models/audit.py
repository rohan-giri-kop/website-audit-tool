from datetime import datetime

from sqlalchemy import (
    JSON,
    Boolean,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.database.session import Base


class Audit(Base):
    __tablename__ = "audits"

    # ============================================================
    # BASIC AUDIT INFORMATION
    # ============================================================

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    website_url: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    # ============================================================
    # AUDIT STATUS
    #
    # IMPORTANT:
    # We do NOT use 0 as a fake/default score.
    #
    # null = analyzer did not produce a result
    # actual number = analyzer produced a real result
    # ============================================================

    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="completed",
    )

    error_message: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    duration_seconds: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    # ============================================================
    # SEO
    # ============================================================

    seo_score: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    seo_metrics: Mapped[dict] = mapped_column(
        JSON,
        default=dict,
        nullable=False,
    )

    # ============================================================
    # PERFORMANCE / LIGHTHOUSE
    # ============================================================

    performance_score: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    performance_metrics: Mapped[dict] = mapped_column(
        JSON,
        default=dict,
        nullable=False,
    )

    # ============================================================
    # SCREENSHOT
    # ============================================================

    screenshot_path: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True,
    )

    # ============================================================
    # ACCESSIBILITY
    # ============================================================

    accessibility_score: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    accessibility_metrics: Mapped[dict] = mapped_column(
        JSON,
        default=dict,
        nullable=False,
    )

    # ============================================================
    # SECURITY
    # ============================================================

    security_score: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    security_metrics: Mapped[dict] = mapped_column(
        JSON,
        default=dict,
        nullable=False,
    )

    # ============================================================
    # MOBILE
    # ============================================================

    mobile_score: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    mobile_metrics: Mapped[dict] = mapped_column(
        JSON,
        default=dict,
        nullable=False,
    )

    # ============================================================
    # UI / UX
    # ============================================================

    uiux_score: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    uiux_metrics: Mapped[dict] = mapped_column(
        JSON,
        default=dict,
        nullable=False,
    )

    # ============================================================
    # PAGE / TECHNICAL DETAILS
    # ============================================================

    page_details: Mapped[dict] = mapped_column(
        JSON,
        default=dict,
        nullable=False,
    )

    # ============================================================
    # OVERALL RESULT
    # ============================================================

    overall_score: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    grade: Mapped[str | None] = mapped_column(
        String(4),
        nullable=True,
    )

    summary: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # ============================================================
    # RECOMMENDATIONS
    #
    # These must come from actual findings/analyzer output.
    # We should NOT create fake recommendations in the model.
    # ============================================================

    recommendations: Mapped[list] = mapped_column(
        JSON,
        default=list,
        nullable=False,
    )

    # ============================================================
    # TIMESTAMPS
    # ============================================================

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    # ============================================================
    # RELATIONSHIPS
    # ============================================================

    user = relationship(
        "User",
        back_populates="audits",
    )

    findings = relationship(
        "Finding",
        back_populates="audit",
        cascade="all, delete-orphan",
    )