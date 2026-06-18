from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# ==========================================
# MySQL Database Configuration
# ==========================================

DB_USER = "root"
DB_PASSWORD = "Rohan050%40"   # @ = %40
DB_HOST = "localhost"
DB_PORT = "3306"
DB_NAME = "website_audit_tool"

DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# ==========================================
# SQLAlchemy Engine
# ==========================================

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    echo=True
)

# ==========================================
# Session Factory
# ==========================================

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# ==========================================
# Base Model
# ==========================================

Base = declarative_base()

# ==========================================
# Initialize Database
# ==========================================

def init_db():
    """
    Import all models here before create_all()
    so SQLAlchemy can detect them.
    """

    from backend.app.models.user import User
    from backend.app.models.audit import Audit
    from backend.app.models.finding import Finding
    from backend.app.models.user_settings import UserSettings

    Base.metadata.create_all(bind=engine)

    print("✅ Database Connected")
    print("✅ Tables Created Successfully")


# ==========================================
# Dependency for FastAPI
# ==========================================

def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()