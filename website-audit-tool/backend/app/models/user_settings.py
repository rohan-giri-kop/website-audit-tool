from sqlalchemy import (
    Boolean,
    ForeignKey,
    Integer,
    String
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

from backend.app.database.session import Base

print("USER SETTINGS MODEL LOADED")


class UserSettings(Base):

    __tablename__ = "user_settings"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        unique=True
    )

    theme: Mapped[str] = mapped_column(
        String(20),
        default="light"
    )

    report_format: Mapped[str] = mapped_column(
        String(20),
        default="pdf"
    )

    default_url: Mapped[str] = mapped_column(
        String(500),
        default=""
    )

    email_notifications: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    weekly_summary: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )