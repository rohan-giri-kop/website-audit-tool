from sqlalchemy import desc
from sqlalchemy.orm import Session

from backend.app.models.notification import Notification


# =====================================================
# GET ALL NOTIFICATIONS
# =====================================================

def get_notifications(
    db: Session,
    user_id: int
):
    return (
        db.query(Notification)
        .filter(Notification.user_id == user_id)
        .order_by(desc(Notification.created_at))
        .all()
    )


# =====================================================
# GET UNREAD COUNT
# =====================================================

def get_unread_count(
    db: Session,
    user_id: int
):
    return (
        db.query(Notification)
        .filter(
            Notification.user_id == user_id,
            Notification.is_read == False
        )
        .count()
    )


# =====================================================
# CREATE NOTIFICATION
# =====================================================

def create_notification(
    db: Session,
    user_id: int,
    title: str,
    message: str,
    notification_type: str = "info"
):
    notification = Notification(
        user_id=user_id,
        title=title,
        message=message,
        type=notification_type,
        is_read=False
    )

    db.add(notification)
    db.commit()
    db.refresh(notification)

    return notification


# =====================================================
# MARK AS READ
# =====================================================

def mark_notification_read(
    db: Session,
    notification_id: int,
    user_id: int
):
    notification = (
        db.query(Notification)
        .filter(
            Notification.id == notification_id,
            Notification.user_id == user_id
        )
        .first()
    )

    if not notification:
        return None

    notification.is_read = True

    db.commit()
    db.refresh(notification)

    return notification


# =====================================================
# MARK ALL AS READ
# =====================================================

def mark_all_notifications_read(
    db: Session,
    user_id: int
):
    notifications = (
        db.query(Notification)
        .filter(
            Notification.user_id == user_id,
            Notification.is_read == False
        )
        .all()
    )

    for notification in notifications:
        notification.is_read = True

    db.commit()

    return len(notifications)


# =====================================================
# DELETE NOTIFICATION
# =====================================================

def delete_notification(
    db: Session,
    notification_id: int,
    user_id: int
):
    notification = (
        db.query(Notification)
        .filter(
            Notification.id == notification_id,
            Notification.user_id == user_id
        )
        .first()
    )

    if not notification:
        return False

    db.delete(notification)
    db.commit()

    return True

def seed_default_notifications(
    db: Session,
    user_id: int
):
    """
    Create default notifications for a new user
    if no notifications exist.
    """

    existing = (
        db.query(Notification)
        .filter(Notification.user_id == user_id)
        .count()
    )

    if existing > 0:
        return

    defaults = [

        Notification(
            user_id=user_id,
            title="Welcome",
            message="Welcome to AI Website Audit Tool.",
            type="success",
            is_read=False
        ),

        Notification(
            user_id=user_id,
            title="Dashboard",
            message="Your dashboard is ready to use.",
            type="info",
            is_read=False
        ),

        Notification(
            user_id=user_id,
            title="Security",
            message="Your account is protected with JWT authentication.",
            type="warning",
            is_read=False
        )

    ]

    db.add_all(defaults)
    db.commit()