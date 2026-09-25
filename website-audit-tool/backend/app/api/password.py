"""
=========================================================
AI WEBSITE AUDIT TOOL
PASSWORD RESET API
=========================================================
"""

from datetime import datetime, timedelta
import secrets

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from sqlalchemy.orm import Session
from passlib.context import CryptContext

from backend.app.database.session import get_db

from backend.app.models.user import User
from backend.app.models.password_reset import PasswordResetToken

from backend.app.schemas.password import (
    ForgotPasswordRequest,
    ResetPasswordRequest,
    PasswordResponse,
)

from backend.app.services.email_service import (
    send_password_reset_email,
)

# =========================================================
# ROUTER
# =========================================================

router = APIRouter()

# =========================================================
# PASSWORD HASHER
# =========================================================

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

# =========================================================
# TOKEN SETTINGS
# =========================================================

TOKEN_EXPIRE_MINUTES = 30

# =========================================================
# GENERATE SECURE TOKEN
# =========================================================

def generate_reset_token() -> str:
    """
    Generate a secure URL-safe token.
    """

    return secrets.token_urlsafe(48)

# =========================================================
# TOKEN EXPIRY
# =========================================================

def token_expiry() -> datetime:
    """
    Token expiry timestamp.
    """

    return datetime.utcnow() + timedelta(
        minutes=TOKEN_EXPIRE_MINUTES
    )

# =========================================================
# PASSWORD HASHING
# =========================================================

def hash_password(password: str) -> str:
    """
    Hash the user's password.
    """

    return pwd_context.hash(password)

# =========================================================
# PASSWORD VERIFY
# =========================================================

def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:
    """
    Verify password.
    """

    return pwd_context.verify(
        plain_password,
        hashed_password
    )

# =========================================================
# FIND USER BY EMAIL
# =========================================================

def get_user_by_email(
    db: Session,
    email: str
):

    return (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

# =========================================================
# FIND RESET TOKEN
# =========================================================

def get_reset_token(
    db: Session,
    token: str
):

    return (
        db.query(PasswordResetToken)
        .filter(
            PasswordResetToken.token == token
        )
        .first()
    )

# =========================================================
# DELETE OLD TOKENS
# =========================================================

def delete_old_tokens(
    db: Session,
    user_id: int
):

    (
        db.query(PasswordResetToken)
        .filter(
            PasswordResetToken.user_id == user_id
        )
        .delete()
    )

    db.commit()

# =========================================================
# CHECK TOKEN VALIDITY
# =========================================================

def validate_token(
    reset_token: PasswordResetToken
):

    if reset_token is None:

        raise HTTPException(

            status_code=status.HTTP_404_NOT_FOUND,

            detail="Invalid password reset link."

        )

    if reset_token.used:

        raise HTTPException(

            status_code=status.HTTP_400_BAD_REQUEST,

            detail="This password reset link has already been used."

        )

    if datetime.utcnow() > reset_token.expires_at:

        raise HTTPException(

            status_code=status.HTTP_400_BAD_REQUEST,

            detail="Password reset link has expired."

        )
        
# =========================================================
# FORGOT PASSWORD
# =========================================================

@router.post(
    "/forgot",
    response_model=PasswordResponse,
    status_code=status.HTTP_200_OK
)
def forgot_password(
    request: ForgotPasswordRequest,
    db: Session = Depends(get_db)
):
    """
    Generate a password reset token and email it to the user.
    """

    # -----------------------------------------------------
    # FIND USER
    # -----------------------------------------------------

    user = get_user_by_email(
        db,
        request.email.lower().strip()
    )

    # -----------------------------------------------------
    # USER NOT FOUND
    # -----------------------------------------------------

    if not user:

        raise HTTPException(

            status_code=status.HTTP_404_NOT_FOUND,

            detail="No account exists with this email address."

        )

    # -----------------------------------------------------
    # REMOVE PREVIOUS TOKENS
    # -----------------------------------------------------

    delete_old_tokens(
        db,
        user.id
    )

    # -----------------------------------------------------
    # CREATE TOKEN
    # -----------------------------------------------------

    token = generate_reset_token()

    expiry = token_expiry()

    # -----------------------------------------------------
    # SAVE TOKEN
    # -----------------------------------------------------

    reset_token = PasswordResetToken(

        user_id=user.id,

        token=token,

        expires_at=expiry,

        used=False

    )

    db.add(reset_token)

    db.commit()

    db.refresh(reset_token)

    # -----------------------------------------------------
    # RESET LINK
    # -----------------------------------------------------

    reset_link = (
        f"http://127.0.0.1:8000/reset-password"
        f"?token={token}"
    )

    # -----------------------------------------------------
    # SEND EMAIL
    # -----------------------------------------------------

    try:

        send_password_reset_email(

            user_email=user.email,

            user_name=user.name,

            reset_link=reset_link

        )

    except Exception as ex:

        # Optional:
        # Roll back token if email sending fails.

        db.delete(reset_token)

        db.commit()

        raise HTTPException(

            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,

            detail=f"Unable to send reset email. {str(ex)}"

        )

    # -----------------------------------------------------
    # SUCCESS
    # -----------------------------------------------------

    return PasswordResponse(

        success=True,

        message=(
            "A password reset link has been sent "
            "to your email address."
        )

    )
    
# =========================================================
# RESET PASSWORD
# =========================================================

@router.post(
    "/reset",
    response_model=PasswordResponse,
    status_code=status.HTTP_200_OK
)
def reset_password(
    request: ResetPasswordRequest,
    db: Session = Depends(get_db)
):
    """
    Reset user password.
    """

    # -----------------------------------------------------
    # PASSWORD MATCH
    # -----------------------------------------------------

    if request.password != request.confirm_password:

        raise HTTPException(

            status_code=status.HTTP_400_BAD_REQUEST,

            detail="Passwords do not match."

        )

    # -----------------------------------------------------
    # FIND TOKEN
    # -----------------------------------------------------

    reset_token = get_reset_token(

        db,

        request.token

    )

    # -----------------------------------------------------
    # VALIDATE TOKEN
    # -----------------------------------------------------

    validate_token(reset_token)

    # -----------------------------------------------------
    # FIND USER
    # -----------------------------------------------------

    user = db.get(

        User,

        reset_token.user_id

    )

    if user is None:

        raise HTTPException(

            status_code=status.HTTP_404_NOT_FOUND,

            detail="User not found."

        )

    # -----------------------------------------------------
    # UPDATE PASSWORD
    # -----------------------------------------------------

    user.password = hash_password(

        request.password

    )

    # -----------------------------------------------------
    # TOKEN USED
    # -----------------------------------------------------

    reset_token.used = True

    # -----------------------------------------------------
    # SAVE
    # -----------------------------------------------------

    db.commit()

    db.refresh(user)

    # -----------------------------------------------------
    # RESPONSE
    # -----------------------------------------------------

    return PasswordResponse(

        success=True,

        message="Password updated successfully."

    )