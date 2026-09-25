"""
Central SQLAlchemy model registry.

Import every model from this module so that all
relationships using string-based model names such as
relationship("Audit") can be resolved reliably.
"""

from backend.app.models.user import User
from backend.app.models.audit import Audit
from backend.app.models.finding import Finding
from backend.app.models.notification import Notification
from backend.app.models.user_settings import UserSettings
from backend.app.models.password_reset import PasswordResetToken
from backend.app.models.contact import Contact


__all__ = [
    "User",
    "Audit",
    "Finding",
    "Notification",
    "UserSettings",
    "PasswordResetToken",
    "Contact",
]