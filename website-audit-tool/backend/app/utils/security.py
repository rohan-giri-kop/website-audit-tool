from datetime import datetime, timedelta, timezone

from jose import jwt
from passlib.context import CryptContext

from backend.app.utils.config import settings
from passlib.exc import UnknownHashError
from datetime import datetime, timedelta, timezone



# =====================================================
# PASSWORD HASHING
# =====================================================

pwd_context = CryptContext(
    schemes=[
        "bcrypt",
        "pbkdf2_sha256"
    ],
    deprecated="auto"
)

def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password, hashed):
    try:
        return pwd_context.verify(password, hashed)
    except UnknownHashError:
        return False

# =====================================================
# JWT TOKEN
# =====================================================

def create_access_token(subject: str):

    now = datetime.now(timezone.utc)

    expire = now + timedelta(
        minutes=settings.access_token_expire_minutes
    )

    payload = {
        "sub": subject,
        "exp": expire,
    }

    token = jwt.encode(
        payload,
        settings.secret_key,
        algorithm=settings.algorithm,
    )

    print("TOKEN CREATED")

    return token