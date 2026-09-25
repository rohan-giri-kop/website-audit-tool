"""
=========================================================
AI WEBSITE AUDIT TOOL
PASSWORD SCHEMAS
=========================================================
"""

from pydantic import BaseModel, EmailStr, Field, field_validator


# =========================================================
# FORGOT PASSWORD REQUEST
# =========================================================

class ForgotPasswordRequest(BaseModel):
    """
    Request model for forgot password.
    """

    email: EmailStr = Field(
        ...,
        description="Registered email address"
    )


# =========================================================
# RESET PASSWORD REQUEST
# =========================================================

class ResetPasswordRequest(BaseModel):
    """
    Request model for resetting password.
    """

    token: str = Field(
        ...,
        min_length=10,
        description="Password reset token"
    )

    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        description="New password"
    )

    confirm_password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        description="Confirm new password"
    )

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:

        if not any(c.isupper() for c in value):
            raise ValueError(
                "Password must contain at least one uppercase letter."
            )

        if not any(c.islower() for c in value):
            raise ValueError(
                "Password must contain at least one lowercase letter."
            )

        if not any(c.isdigit() for c in value):
            raise ValueError(
                "Password must contain at least one number."
            )

        special_characters = "!@#$%^&*()_+-=[]{}|;:',.<>?/`~"

        if not any(c in special_characters for c in value):
            raise ValueError(
                "Password must contain at least one special character."
            )

        return value

    @field_validator("confirm_password")
    @classmethod
    def validate_confirm_password(cls, value: str) -> str:

        if len(value.strip()) == 0:
            raise ValueError(
                "Confirm password is required."
            )

        return value


# =========================================================
# PASSWORD RESET RESPONSE
# =========================================================

class PasswordResponse(BaseModel):
    """
    Standard password API response.
    """

    success: bool

    message: str