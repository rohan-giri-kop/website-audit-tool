from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.database.session import Base


class Finding(Base):
    __tablename__ = "findings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    audit_id: Mapped[int] = mapped_column(
        ForeignKey("audits.id"),
        nullable=False,
        index=True
    )

    category: Mapped[str] = mapped_column(String(100), nullable=False)

    title: Mapped[str] = mapped_column(String(255), nullable=False)

    severity: Mapped[str] = mapped_column(String(20), nullable=False)

    description: Mapped[str] = mapped_column(Text, default="")

    issue: Mapped[str] = mapped_column(Text, nullable=False)

    recommendation: Mapped[str] = mapped_column(Text, nullable=False)

    priority: Mapped[str] = mapped_column(String(20), nullable=False)

    benefit: Mapped[str] = mapped_column(Text, default="")

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    audit = relationship("Audit", back_populates="findings")