from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.database.session import get_db
from backend.app.models.user_settings import UserSettings
from backend.app.api.auth import get_current_user

router = APIRouter()
print("SETTINGS API LOADED")

@router.get("")
def get_settings(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    settings = (
        db.query(UserSettings)
        .filter(
            UserSettings.user_id ==
            current_user.id
        )
        .first()
    )

    if not settings:

        settings = UserSettings(
            user_id=current_user.id
        )

        db.add(settings)
        db.commit()
        db.refresh(settings)

    return settings

@router.put("")
def update_settings(
    payload: dict,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    settings = (
        db.query(UserSettings)
        .filter(
            UserSettings.user_id ==
            current_user.id
        )
        .first()
    )

    if not settings:

        settings = UserSettings(
            user_id=current_user.id
        )

        db.add(settings)

    settings.theme = payload.get(
        "theme",
        "light"
    )

    settings.report_format = payload.get(
        "report_format",
        "pdf"
    )

    settings.default_url = payload.get(
        "default_url",
        ""
    )

    settings.email_notifications = payload.get(
        "email_notifications",
        True
    )

    settings.weekly_summary = payload.get(
        "weekly_summary",
        False
    )

    db.commit()

    return {
        "message":
        "Settings updated"
    }