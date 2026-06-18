from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.models.user import User
from backend.app.utils.security import create_access_token, hash_password, verify_password

def get_user_by_email(db: Session, email: str) -> User | None:
    return db.execute(select(User).where(User.email == email)).scalar_one_or_none()


def create_user(db: Session, name: str, email: str, password: str) -> User:
    user = User(name=name, email=email, password=hash_password(password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, email: str, password: str) -> User | None:
    user = get_user_by_email(db, email)
    if not user or not verify_password(password, user.password):
        return None
    return user


def issue_token(user: User) -> str:
    return create_access_token(str(user.id))
