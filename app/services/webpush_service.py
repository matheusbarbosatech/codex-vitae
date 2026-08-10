import json
import logging
from typing import List, Dict, Any, Optional

try:
    from pywebpush import webpush, WebPushException
    PYWEBPUSH_AVAILABLE = True
except ImportError:
    webpush = None
    WebPushException = Exception
    PYWEBPUSH_AVAILABLE = False

from app.core.config import settings
from app.models.user import PushSubscription, User
from app.schemas.notification import NotificationPayload
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)


def send_webpush_notification(
    subscription: PushSubscription,
    payload: NotificationPayload
) -> bool:
    """
    Sends a Web Push Notification to a single browser subscription using pywebpush and VAPID.
    """
    sub_info = {
        "endpoint": subscription.endpoint,
        "keys": {
            "p256dh": subscription.p256dh,
            "auth": subscription.auth
        }
    }

    payload_json = json.dumps({
        "title": payload.title,
        "body": payload.body,
        "icon": payload.icon or "/static/img/icon-192.png",
        "url": payload.url or "/dashboard",
        "data": payload.data or {}
    })

    if not PYWEBPUSH_AVAILABLE:
        logger.info(f"💡 [Mock WebPush Dispatch] Para: {subscription.endpoint[:40]}... Title: '{payload.title}', Body: '{payload.body}'")
        return True

    try:
        webpush(
            subscription_info=sub_info,
            data=payload_json,
            vapid_private_key=settings.VAPID_PRIVATE_KEY,
            vapid_claims={"sub": settings.VAPID_CLAIM_EMAIL}
        )
        logger.info(f"✔ WebPush enviado com sucesso para {subscription.endpoint[:40]}...")
        return True
    except WebPushException as ex:
        logger.error(f"❌ Erro ao enviar WebPush: {ex}")
        if ex.response and ex.response.status_code in [404, 410]:
            # Subscription has expired or un-subscribed
            logger.info("Assinatura push expirada. Deve ser removida do DB.")
        return False
    except Exception as e:
        logger.error(f"Erro inesperado ao enviar WebPush: {e}")
        return False


def dispatch_push_to_user(user: User, payload: NotificationPayload, db: Session) -> int:
    """
    Dispatches push notification to all active browser subscriptions for a user.
    """
    subscriptions = db.query(PushSubscription).filter(PushSubscription.user_id == user.id).all()
    if not subscriptions:
        logger.info(f"Nenhuma assinatura push encontrada para o usuário {user.email}.")
        return 0

    success_count = 0
    for sub in subscriptions:
        if send_webpush_notification(sub, payload):
            success_count += 1

    return success_count
