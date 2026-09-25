from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.api.auth import get_current_user
from backend.app.database.session import get_db
from backend.app.models.user import User
from backend.app.schemas.notification import (
    NotificationList,
    NotificationRead,
)
from backend.app.services.notification_service import (
    get_notifications,
    get_unread_count,
    mark_notification_read,
    mark_all_notifications_read,
    delete_notification,
)
from backend.app.services.notification_service import seed_default_notifications

router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"]
)


# =====================================================
# GET ALL NOTIFICATIONS
# =====================================================

@router.get(
    "",
    response_model=NotificationList
)
def list_notifications(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    
    seed_default_notifications(
        db,
        current_user.id
    )

    notifications = get_notifications(
        db,
        current_user.id
    )

    unread = get_unread_count(
        db,
        current_user.id
    )

    return NotificationList(
        total=len(notifications),
        unread=unread,
        notifications=notifications
    )
    
    
    
# =====================================================
# GET UNREAD NOTIFICATION COUNT
# =====================================================

@router.get("/unread-count")
def unread_notification_count(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    count = get_unread_count(
        db,
        current_user.id
    )

    return {
        "count": count
    }


# =====================================================
# MARK SINGLE NOTIFICATION AS READ
# =====================================================



@router.put(
    "/{notification_id}/read",
    response_model=NotificationRead
)
def read_notification(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    notification = mark_notification_read(
        db,
        notification_id,
        current_user.id
    )

    if notification is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found"
        )

    return notification


# =====================================================
# MARK ALL NOTIFICATIONS AS READ
# =====================================================

@router.put("/read-all")
def read_all_notifications(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    updated = mark_all_notifications_read(
        db,
        current_user.id
    )

    return {
        "success": True,
        "updated": updated,
        "message": "All notifications marked as read."
    }


# =====================================================
# DELETE NOTIFICATION
# =====================================================

@router.delete("/{notification_id}")
def remove_notification(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    success = delete_notification(
        db,
        notification_id,
        current_user.id
    )

    if not success:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found"
        )

    return {
        "success": True,
        "message": "Notification deleted successfully."
    }