"""
=========================================================
AI WEBSITE AUDIT TOOL
PASSWORD RESET MODEL
=========================================================
"""

from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
)

from sqlalchemy.orm import relationship

from backend.app.database.session import Base


class PasswordResetToken(Base):
    """
    Stores password reset tokens.
    """

    __tablename__ = "password_reset_tokens"

    # -----------------------------------------------------
    # PRIMARY KEY
    # -----------------------------------------------------

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # -----------------------------------------------------
    # USER
    # -----------------------------------------------------

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # -----------------------------------------------------
    # RESET TOKEN
    # -----------------------------------------------------

    token = Column(
        String(255),
        unique=True,
        nullable=False,
        index=True
    )

    # -----------------------------------------------------
    # EXPIRATION
    # -----------------------------------------------------

    expires_at = Column(
        DateTime,
        nullable=False
    )

    # -----------------------------------------------------
    # USED STATUS
    # -----------------------------------------------------

    used = Column(
        Boolean,
        default=False,
        nullable=False
    )

    # -----------------------------------------------------
    # CREATED
    # -----------------------------------------------------

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    # -----------------------------------------------------
    # RELATIONSHIP
    # -----------------------------------------------------

    user = relationship(
        "User",
        back_populates="password_reset_tokens"
    )

    # -----------------------------------------------------
    # STRING
    # -----------------------------------------------------

    def __repr__(self):

        return (
            f"<PasswordResetToken("
            f"user_id={self.user_id}, "
            f"used={self.used})>"
        )