from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


# ==========================================================
# PROJECT ROOT
# ==========================================================

# session.py location:
#
# website-audit-tool/
# └── backend/
#     └── app/
#         └── database/
#             └── session.py
#
# parents[3] = website-audit-tool

PROJECT_ROOT = Path(__file__).resolve().parents[3]


# ==========================================================
# DATABASE PATH
# ==========================================================

# The SQLite database is intentionally outside the project
# directory because this is the existing project database
# already used by Alembic.

DATABASE_PATH = PROJECT_ROOT.parent / "website_audit_tool.db"

DATABASE_URL = f"sqlite:///{DATABASE_PATH.as_posix()}"


# ==========================================================
# ENGINE
# ==========================================================

engine = create_engine(
    DATABASE_URL,
    connect_args={
        "check_same_thread": False,
    },
)


# ==========================================================
# SESSION
# ==========================================================

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


# ==========================================================
# BASE
# ==========================================================

Base = declarative_base()


# ==========================================================
# LOAD ALL MODELS
# ==========================================================

# IMPORTANT:
#
# This must happen AFTER Base is created.
#
# It registers every SQLAlchemy model and makes relationships
# such as relationship("Audit"), relationship("Finding"), etc.
# resolvable throughout the application.

from backend.app import models as _models  # noqa: E402,F401


# ==========================================================
# DATABASE INITIALIZATION
# ==========================================================

def init_db():
    """
    Initialize the application's model registry.

    Database schema changes are handled by Alembic.
    We deliberately do NOT call Base.metadata.create_all()
    here.
    """

    # Force access to the registry so model imports are complete.
    _ = _models

    print("=" * 60)
    print("DATABASE")
    print("=" * 60)
    print(f"Database path : {DATABASE_PATH}")
    print(f"Database URL  : {DATABASE_URL}")
    print(
        "Registered tables:",
        list(Base.metadata.tables.keys()),
    )
    print("=" * 60)


# ==========================================================
# DATABASE DEPENDENCY
# ==========================================================

def get_db():
    """
    FastAPI database dependency.
    """

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()