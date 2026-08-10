import json
import logging
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, Request, Depends, status
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.base import Base
from app.db.session import engine, get_db
from app.models.user import User, CodexPlan
from app.core.security import get_current_user_optional
from app.services.codex_service import CODEX_MODULES_CATALOG, get_user_plans
from app.services.stripe_service import check_and_update_user_trial_status
from app.api.auth import router as auth_router
from app.api.billing import router as billing_router
from app.api.codex_modules import router as codex_router
from app.api.growth import router as growth_router
from app.api.notifications import router as notifications_router

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("codex_vitae")

# Create database tables automatically in SQLite/Dev environment
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Codex Vitae Life OS — O Sistema Operacional para a Vida com PWA, Push Notifications VAPID & IA Open-Source.",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Static & Templates setup
BASE_DIR = Path(__file__).resolve().parent
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# Mount API V1 Routers
app.include_router(auth_router, prefix=settings.API_V1_STR)
app.include_router(billing_router, prefix=settings.API_V1_STR)
app.include_router(codex_router, prefix=settings.API_V1_STR)
app.include_router(growth_router, prefix=settings.API_V1_STR)
app.include_router(notifications_router, prefix=settings.API_V1_STR)


def render_template(request: Request, name: str, context: dict) -> HTMLResponse:
    ctx = {"request": request, **context}
    try:
        return templates.TemplateResponse(request=request, name=name, context=ctx)
    except TypeError:
        return templates.TemplateResponse(name, ctx)


# Root Scope Service Worker Serving
@app.get("/sw.js", include_in_schema=False)
def serve_service_worker():
    sw_path = BASE_DIR / "static" / "sw.js"
    return FileResponse(sw_path, media_type="application/javascript")


# HTML WEB VIEWS (Jinja2 Rendered Pages)

@app.get("/", response_class=HTMLResponse)
def index_view(request: Request, user: Optional[User] = Depends(get_current_user_optional)):
    """Landing Page de Alta Conversão"""
    return render_template(request, "index.html", {
        "user": user,
        "modules": CODEX_MODULES_CATALOG
    })


@app.get("/onboarding", response_class=HTMLResponse)
def onboarding_view(request: Request, user: Optional[User] = Depends(get_current_user_optional)):
    """Diagnóstico Interativo em 4 Passos (Momento Aha Sem Atritos)"""
    return render_template(request, "onboarding.html", {"user": user})


@app.get("/login", response_class=HTMLResponse)
def login_view(request: Request, user: Optional[User] = Depends(get_current_user_optional)):
    """Login Page"""
    if user:
        return RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)
    return render_template(request, "login.html", {"user": None})


@app.get("/register", response_class=HTMLResponse)
def register_view(request: Request, user: Optional[User] = Depends(get_current_user_optional)):
    """Registration Page (14-Day Reverse Trial)"""
    if user:
        return RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)
    return render_template(request, "register.html", {"user": None})


@app.get("/auditor-burnout", response_class=HTMLResponse)
def burnout_auditor_view(request: Request, user: Optional[User] = Depends(get_current_user_optional)):
    """Engineering-as-Marketing Lead Magnet: Auditor de Burnout Biométrico"""
    return render_template(request, "burnout_auditor.html", {"user": user})


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard_view(
    request: Request,
    user: Optional[User] = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    """User Dashboard Area"""
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)

    check_and_update_user_trial_status(user, db)

    plans = get_user_plans(user, db)
    plans_data = [
        {
            "id": p.id,
            "module_key": p.module_key,
            "module_title": p.module_title,
            "plan_output": p.plan_output,
            "created_at": p.created_at.strftime("%d/%m/%Y %H:%M")
        } for p in plans
    ]

    return render_template(request, "dashboard.html", {
        "user": user,
        "modules": CODEX_MODULES_CATALOG,
        "plans": plans,
        "plans_json": json.dumps(plans_data)
    })


@app.get("/logout")
def logout_view(request: Request):
    response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    response.delete_cookie("access_token")
    return response


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "app": settings.PROJECT_NAME,
        "version": settings.VERSION
    }
