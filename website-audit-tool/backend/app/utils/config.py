from os import getenv
from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv()

class Settings(BaseModel):

    # =====================================================
    # APPLICATION
    # =====================================================

    app_name: str = Field(
        default_factory=lambda: getenv(
            "APP_NAME",
            "AI Website Audit Tool"
        )
    )

    app_base_url: str = Field(
        default_factory=lambda: getenv(
            "APP_BASE_URL",
            "http://127.0.0.1:8000"
        )
    )

    # =====================================================
    # SECURITY
    # =====================================================

    secret_key: str = Field(
        default_factory=lambda: getenv(
            "SECRET_KEY",
            "change-me"
        )
    )

    algorithm: str = Field(
        default_factory=lambda: getenv(
            "ALGORITHM",
            "HS256"
        )
    )

    access_token_expire_minutes: int = Field(
        default_factory=lambda: int(
            getenv(
                "ACCESS_TOKEN_EXPIRE_MINUTES",
                "120"
            )
        )
    )

    # =====================================================
    # DATABASE
    # =====================================================

    database_url: str = Field(
        default_factory=lambda: getenv(
            "DATABASE_URL",
            "sqlite:///website_audit_tool.db"
        )
    )

    # =====================================================
    # CORS
    # =====================================================

    backend_cors_origins: list[str] = Field(
        default_factory=lambda: [
            origin.strip()
            for origin in getenv(
                "BACKEND_CORS_ORIGINS",
                "http://localhost:8000"
            ).split(",")
            if origin.strip()
        ]
    )

    # =====================================================
    # GMAIL SMTP
    # =====================================================

    email_host: str = Field(
        default_factory=lambda: getenv(
            "EMAIL_HOST",
            "smtp.gmail.com"
        )
    )

    email_port: int = Field(
        default_factory=lambda: int(
            getenv(
                "EMAIL_PORT",
                "587"
            )
        )
    )

    email_address: str = Field(
        default_factory=lambda: getenv(
            "EMAIL_ADDRESS",
            ""
        )
    )

    email_password: str = Field(
        default_factory=lambda: getenv(
            "EMAIL_PASSWORD",
            ""
        )
    )

    email_from: str = Field(
        default_factory=lambda: getenv(
            "EMAIL_FROM",
            "AI Website Audit Tool"
        )
    )


settings = Settings()