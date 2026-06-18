from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from fastapi.staticfiles import StaticFiles

from fastapi.templating import Jinja2Templates

from backend.app.api import auth, audits, reports, ui
from backend.app.database.session import init_db
from backend.app.utils.config import settings
from fastapi.staticfiles import StaticFiles
from backend.app.api.settings import router as settings_router

from pathlib import Path


app = FastAPI(title=settings.app_name, version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.backend_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent.parent

app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "frontend" / "static"),
    name="static"
)

app.mount(
    "/reports",
    StaticFiles(directory="reports"),
    name="reports"
)



templates = Jinja2Templates(
    directory=str(BASE_DIR / "frontend" / "templates")
)

@app.on_event("startup")
def on_startup() -> None:
    pass


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(audits.router, prefix="/api/audits", tags=["audits"])
app.include_router(reports.router, prefix="/api/reports", tags=["reports"])
app.include_router(ui.router, tags=["ui"])
app.include_router(
    settings_router,
    prefix="/api/settings",
    tags=["settings"]
)

@app.exception_handler(404)
async def not_found(_: Request, __: Exception):
    return HTMLResponse(templates.get_template("404.html").render(), status_code=404)
