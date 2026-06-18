from datetime import datetime
from sqlalchemy import JSON

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text, func, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.database.session import Base


class Audit(Base):
    __tablename__ = "audits"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    website_url: Mapped[str] = mapped_column(String(500), nullable=False)
    seo_score: Mapped[float] = mapped_column(Float, default=0)
    performance_score: Mapped[float] = mapped_column(Float, default=0)
    screenshot_path = Column(String, nullable=True)
    accessibility_score: Mapped[float] = mapped_column(Float, default=0)
    
    accessibility_metrics: Mapped[dict] = mapped_column(
        JSON,
        default=dict
    )
    
    security_score: Mapped[float] = mapped_column(Float, default=0)
    security_metrics: Mapped[dict] = mapped_column(
        JSON,
        default=dict
    )
    mobile_score: Mapped[float] = mapped_column(Float, default=0)
    mobile_metrics: Mapped[dict] = mapped_column(
        JSON,
        default=dict
    )
    overall_score: Mapped[float] = mapped_column(Float, default=0)
    summary: Mapped[str] = mapped_column(Text, default="")
    recommendations: Mapped[list] = mapped_column(
            JSON,
            default=list
        )
    grade: Mapped[str] = mapped_column(String(4), default="F")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="audits")
    findings = relationship("Finding", back_populates="audit", cascade="all, delete-orphan")
