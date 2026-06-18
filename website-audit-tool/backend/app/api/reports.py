from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from backend.app.database.session import get_db
from backend.app.models.user import User
from backend.app.reports.generator import build_pdf_report
from backend.app.services.audit_service import get_audit
from backend.app.utils.config import settings


router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def _current_user_id(token: str = Depends(oauth2_scheme)) -> int:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        return int(payload.get("sub"))
    except (JWTError, TypeError, ValueError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication token")


@router.get("/{audit_id}/pdf")
def download_pdf(
    audit_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(_current_user_id)
):

    if not db.get(User, user_id):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    audit = get_audit(
        db,
        audit_id,
        user_id
    )

    if not audit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Audit not found"
        )

    pdf_bytes = build_pdf_report(
        audit,
        audit.findings
    )

    filename = f"audit-report-{audit.id}.pdf"

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition":
            f'attachment; filename="{filename}"'
        }
    )