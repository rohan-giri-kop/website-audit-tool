from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from backend.app.database.session import get_db
from backend.app.models.user import User
from backend.app.schemas.audit import AuditRead, AuditRequest
from backend.app.services.audit_service import create_audit, get_audit, list_audits
from backend.app.utils.config import settings


router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def _current_user_id(token: str = Depends(oauth2_scheme)) -> int:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        return int(payload.get("sub"))
    except (JWTError, TypeError, ValueError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication token")


@router.post("", response_model=AuditRead, status_code=status.HTTP_201_CREATED)
def analyze(payload: AuditRequest, db: Session = Depends(get_db), user_id: int = Depends(_current_user_id)):
    if not db.get(User, user_id):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return create_audit(db, user_id, payload)


@router.get("", response_model=list[AuditRead])
def history(db: Session = Depends(get_db), user_id: int = Depends(_current_user_id)):
    return list_audits(db, user_id)


@router.get("/{audit_id}", response_model=AuditRead)
def detail(audit_id: int, db: Session = Depends(get_db), user_id: int = Depends(_current_user_id)):
    audit = get_audit(db, audit_id, user_id)
    if not audit:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Audit not found")
    return audit
