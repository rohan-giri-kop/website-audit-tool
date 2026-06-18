from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


router = APIRouter()
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

templates = Jinja2Templates(
    directory=str(BASE_DIR / "frontend" / "templates")
)

@router.get("/", response_class=HTMLResponse)
def landing(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "page_title": "Analyze Any Website in Seconds"
        }
    )

@router.get("/login", response_class=HTMLResponse)
def login(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={
            "page_title": "Login"
        }
    )


@router.get("/register", response_class=HTMLResponse)
def register(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="register.html",
        context={
            "page_title": "Register"
        }
    )    
    
@router.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "page_title": "Dashboard"
        }
    )


@router.get("/audits/new", response_class=HTMLResponse)
def new_audit(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="new_audit.html",
        context={
            "page_title": "New Audit"
        }
    )


@router.get("/audits/{audit_id}", response_class=HTMLResponse)
def audit_report(request: Request, audit_id: int):
    return templates.TemplateResponse(
        request=request,
        name="report.html",
        context={
            "page_title": f"Audit #{audit_id}",
            "audit_id": audit_id
        }
    )


@router.get("/history", response_class=HTMLResponse)
def history(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="history.html",
        context={
            "page_title": "Audit History"
        }
    )


@router.get("/profile", response_class=HTMLResponse)
def profile(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="profile.html",
        context={
            "page_title": "Profile"
        }
    )


@router.get("/settings", response_class=HTMLResponse)
def settings_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="settings.html",
        context={
            "page_title": "Settings"
        }
    )


@router.get("/404", response_class=HTMLResponse)
def not_found(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="404.html",
        context={
            "page_title": "Not Found"
        },
        status_code=404
    )
