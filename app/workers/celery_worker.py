import logging
import asyncio
try:
    from celery import Celery
    CELERY_AVAILABLE = True
except ImportError:
    Celery = None
    CELERY_AVAILABLE = False

from app.core.config import settings
from app.db.session import SessionLocal
from app.models.user import User
from app.services.sentinel_engine import run_sentinel_analysis_for_user
from app.schemas.notification import NotificationPayload
from app.services.webpush_service import dispatch_push_to_user

logger = logging.getLogger(__name__)

if CELERY_AVAILABLE:
    celery_app = Celery(
        "codex_sentinel",
        broker=settings.CELERY_BROKER_URL,
        backend=settings.CELERY_RESULT_BACKEND
    )
    celery_app.conf.update(
        task_serializer="json",
        accept_content=["json"],
        result_serializer="json",
        timezone="UTC",
        enable_utc=True,
    )
else:
    celery_app = None


def run_sentinel_monitor_task_sync(user_id: int):
    """
    Synchronous / Celery worker handler for Sentinel Engine analysis.
    """
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            logger.error(f"Usuário ID {user_id} não encontrado para análise do Sentinela.")
            return {"error": "user_not_found"}

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(run_sentinel_analysis_for_user(user, db))
        loop.close()

        logger.info(f"✔ Análise do Modo Sentinela concluída para {user.email}: {result['status']}")
        return result
    finally:
        db.close()


if CELERY_AVAILABLE and celery_app:
    @celery_app.task(name="sentinel.monitor_biometrics")
    def run_sentinel_monitor_task(user_id: int):
        return run_sentinel_monitor_task_sync(user_id)

    @celery_app.task(name="sentinel.dispatch_push")
    def dispatch_push_notification_task(user_id: int, title: str, body: str):
        db = SessionLocal()
        try:
            user = db.query(User).filter(User.id == user_id).first()
            if user:
                payload = NotificationPayload(title=title, body=body)
                count = dispatch_push_to_user(user, payload, db)
                return {"delivered_count": count}
            return {"error": "user_not_found"}
        finally:
            db.close()
