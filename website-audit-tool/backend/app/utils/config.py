from os import getenv

from pydantic import BaseModel, Field


class Settings(BaseModel):
    secret_key: str = Field(default_factory=lambda: getenv("SECRET_KEY", "change-me"))
    algorithm: str = Field(default_factory=lambda: getenv("ALGORITHM", "HS256"))
    access_token_expire_minutes: int = Field(default_factory=lambda: int(getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "120")))
    database_url: str = Field(
    default_factory=lambda: getenv(
        "DATABASE_URL",
        "mysql+pymysql://root:Rohan050%40@localhost:3306/website_audit_tool"
        )
    )  
    backend_cors_origins: list[str] = Field(
            default_factory=lambda: [
                origin.strip()
                for origin in getenv("BACKEND_CORS_ORIGINS", "http://localhost:8000").split(",")
                if origin.strip()
            ]
        )
    app_name: str = Field(default_factory=lambda: getenv("APP_NAME", "AI Website Audit Tool"))
    app_base_url: str = Field(default_factory=lambda: getenv("APP_BASE_URL", "http://localhost:8000"))


settings = Settings()
