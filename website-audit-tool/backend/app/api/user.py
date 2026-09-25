"""
==========================================================
User API
AI Website Audit Tool
==========================================================
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from backend.app.api.auth import get_current_user
from backend.app.database.session import get_db
from backend.app.models.user import User
from backend.app.models.user_settings import UserSettings


# ==========================================================
# ROUTER
# ==========================================================

router = APIRouter(

    prefix="/api/user",

    tags=["User"]

)


# ==========================================================
# HELPERS
# ==========================================================

def success_response(

    data: Any,

    message: str = "Success"

) -> dict:

    return {

        "success": True,

        "message": message,

        "timestamp": datetime.utcnow().isoformat(),

        "data": data

    }


def error_response(

    message: str,

    status_code: int = 400

):

    raise HTTPException(

        status_code=status_code,

        detail=message

    )


# ==========================================================
# USER SERVICE
# ==========================================================

class UserService:

    def __init__(

        self,

        db: Session,

        current_user: User

    ):

        self.db = db

        self.current_user = current_user

    @property
    def user_id(self):

        return self.current_user.id


# ==========================================================
# DEPENDENCY
# ==========================================================

def get_user_service(

    db: Session = Depends(get_db),

    current_user: User = Depends(

        get_current_user

    )

):

    return UserService(

        db=db,

        current_user=current_user

    )
    
# ==========================================================
# USER PROFILE
# ==========================================================

class UserService(UserService):

    def get_profile(self):

        settings = (

            self.db.query(UserSettings)

            .filter(

                UserSettings.user_id ==

                self.user_id

            )

            .first()

        )

        audit_count = (

            self.current_user.audits

        )

        return {

            "id":

                self.current_user.id,

            "name":

                self.current_user.name,

            "email":

                self.current_user.email,

            "created_at":

                self.current_user.created_at.isoformat(),

            "audit_count":

                len(audit_count),

            "settings":{

                "theme":

                    settings.theme

                    if settings

                    else "light",

                "report_format":

                    settings.report_format

                    if settings

                    else "pdf",

                "default_url":

                    settings.default_url

                    if settings

                    else "",

                "email_notifications":

                    settings.email_notifications

                    if settings

                    else True,

                "weekly_summary":

                    settings.weekly_summary

                    if settings

                    else False

            }

        }


# ==========================================================
# GET USER PROFILE
# ==========================================================

@router.get("/profile")

def get_profile(

    service: UserService = Depends(

        get_user_service

    )

):

    return success_response(

        data=

            service.get_profile(),

        message=

            "User profile loaded."

    )
    
# ==========================================================
# USER PREFERENCES
# ==========================================================

class UserService(UserService):

    def get_preferences(self) -> dict:
        """
        Return user preferences.
        """

        settings = (

            self.db.query(UserSettings)

            .filter(

                UserSettings.user_id ==

                self.user_id

            )

            .first()

        )

        if settings is None:

            settings = UserSettings(

                user_id=self.user_id

            )

            self.db.add(settings)

            self.db.commit()

            self.db.refresh(settings)

        return {

            "theme":

                settings.theme,

            "report_format":

                settings.report_format,

            "default_url":

                settings.default_url,

            "email_notifications":

                settings.email_notifications,

            "weekly_summary":

                settings.weekly_summary

        }


# ==========================================================
# GET USER PREFERENCES
# ==========================================================

@router.get("/preferences")

def get_user_preferences(

    service: UserService = Depends(

        get_user_service

    )

):
    """
    Return user preferences.
    """

    preferences = service.get_preferences()

    return success_response(

        data=preferences,

        message="User preferences loaded."

    )

# ==========================================================
# UPDATE USER PREFERENCES
# ==========================================================

class UserService(UserService):

    def update_preferences(

        self,

        data: dict

    ) -> dict:
        """
        Update user preferences.
        """

        settings = (

            self.db.query(UserSettings)

            .filter(

                UserSettings.user_id ==

                self.user_id

            )

            .first()

        )

        if settings is None:

            settings = UserSettings(

                user_id=self.user_id

            )

            self.db.add(settings)

        if "theme" in data:

            settings.theme = data["theme"]

        if "report_format" in data:

            settings.report_format = data["report_format"]

        if "default_url" in data:

            settings.default_url = data["default_url"]

        if "email_notifications" in data:

            settings.email_notifications = bool(

                data["email_notifications"]

            )

        if "weekly_summary" in data:

            settings.weekly_summary = bool(

                data["weekly_summary"]

            )

        self.db.commit()

        self.db.refresh(settings)

        return {

            "theme": settings.theme,

            "report_format": settings.report_format,

            "default_url": settings.default_url,

            "email_notifications": settings.email_notifications,

            "weekly_summary": settings.weekly_summary

        }


# ==========================================================
# UPDATE USER PREFERENCES API
# ==========================================================

@router.put("/preferences")

def update_user_preferences(

    data: dict,

    service: UserService = Depends(

        get_user_service

    )

):
    """
    Update user preferences.
    """

    preferences = service.update_preferences(

        data

    )

    return success_response(

        data=preferences,

        message="User preferences updated."

    )
    
# ==========================================================
# USER THEME
# ==========================================================

class UserService(UserService):

    def get_theme(self) -> dict:
        """
        Return the active theme for the current user.
        """

        settings = (

            self.db.query(UserSettings)

            .filter(

                UserSettings.user_id ==

                self.user_id

            )

            .first()

        )

        if settings is None:

            settings = UserSettings(

                user_id=self.user_id

            )

            self.db.add(settings)

            self.db.commit()

            self.db.refresh(settings)

        return {

            "theme": settings.theme

        }


# ==========================================================
# GET USER THEME
# ==========================================================

@router.get("/theme")

def get_user_theme(

    service: UserService = Depends(

        get_user_service

    )

):
    """
    Return the current user's active theme.
    """

    theme = service.get_theme()

    return success_response(

        data=theme,

        message="User theme loaded."

    )
    
# ==========================================================
# USER HEALTH
# ==========================================================

@router.get("/health")
def user_health():
    """
    User API health check.
    """

    return {

        "success": True,

        "service": "user",

        "status": "healthy",

        "timestamp": datetime.utcnow().isoformat()

    }


# ==========================================================
# USER API INFORMATION
# ==========================================================

@router.get("")
def user_api_info():
    """
    User API information.
    """

    return {

        "service": "User API",

        "version": "1.0.0",

        "available_routes": [

            "/profile",

            "/preferences",

            "/theme",

            "/health"

        ]

    }


# ==========================================================
# VALIDATION HELPERS
# ==========================================================

def validate_theme(

    theme: str

) -> str:
    """
    Validate theme value.
    """

    allowed = {

        "light",

        "dark",

        "system"

    }

    theme = (

        theme or "light"

    ).lower()

    if theme not in allowed:

        return "light"

    return theme


def validate_report_format(

    report_format: str

) -> str:
    """
    Validate report format.
    """

    allowed = {

        "pdf",

        "html"

    }

    report_format = (

        report_format or "pdf"

    ).lower()

    if report_format not in allowed:

        return "pdf"

    return report_format


# ==========================================================
# INITIALIZE DEFAULT SETTINGS
# ==========================================================

class UserService(UserService):

    def initialize_settings(self) -> None:
        """
        Ensure the current user has a settings record.
        """

        settings = (

            self.db.query(UserSettings)

            .filter(

                UserSettings.user_id ==

                self.user_id

            )

            .first()

        )

        if settings is None:

            settings = UserSettings(

                user_id=self.user_id

            )

            self.db.add(settings)

            self.db.commit()