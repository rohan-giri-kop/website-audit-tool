from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates


router = APIRouter()


# ==========================================================
# TEMPLATE LOCATION
# ==========================================================

BASE_DIR = Path(__file__).resolve().parents[3]

templates = Jinja2Templates(
    directory=str(
        BASE_DIR / "frontend" / "templates"
    )
)


# ==========================================================
# NOTIFICATIONS PAGE
# ==========================================================

@router.get("/notifications")
async def notifications_page(
    request: Request
):

    return templates.TemplateResponse(
        request=request,
        name="notifications.html",
        context={
            "request": request,
            "page_title": "Notifications",
        },
    )