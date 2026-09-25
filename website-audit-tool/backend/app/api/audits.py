from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.database.session import get_db
from backend.app.models.user import User
from backend.app.schemas.audit import AuditRead, AuditRequest
from backend.app.services.audit_service import (
    create_audit,
    get_audit,
    list_audits,
)
from backend.app.api.auth import get_current_user


router = APIRouter()


# ==========================================================
# CREATE NEW AUDIT
# ==========================================================

@router.post(
    "",
    response_model=AuditRead,
    status_code=status.HTTP_201_CREATED,
)
def analyze(
    payload: AuditRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Create a new website audit for the authenticated user.
    """

    website_url = str(
        payload.website_url
    ).strip()


    if not website_url:

        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Website URL is required",
        )


    return create_audit(
        db=db,
        user_id=current_user.id,
        website_url=website_url,
    )


# ==========================================================
# GET AUDIT HISTORY
# ==========================================================

@router.get(
    "",
    response_model=list[AuditRead],
)
def history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Return all audits belonging to the logged-in user.
    """

    return list_audits(
        db,
        current_user.id,
    )


# ==========================================================
# GET SINGLE AUDIT
# ==========================================================

@router.get(
    "/{audit_id}",
    response_model=AuditRead,
)
def detail(
    audit_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Return one audit belonging to the logged-in user.
    """

    audit = get_audit(
        db,
        audit_id,
        current_user.id,
    )


    if not audit:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Audit not found",
        )


    return audit