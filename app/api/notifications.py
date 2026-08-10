from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User, PushSubscription
from app.core.config import settings
from app.core.security import get_current_user
from app.schemas.notification import (
    PushSubscriptionCreate,
    PushSubscriptionResponse,
    VapidKeyResponse
)
from app.services.sentinel_engine import run_sentinel_analysis_for_user

router = APIRouter(prefix="/notifications", tags=["Notificações Push PWA & VAPID"])


@router.get("/vapid-public-key", response_model=VapidKeyResponse)
def get_vapid_public_key():
    """
    Returns the VAPID Public Key for client-side PWA subscription.
    """
    return VapidKeyResponse(public_key=settings.VAPID_PUBLIC_KEY)


@router.post("/subscribe", response_model=PushSubscriptionResponse, status_code=status.HTTP_201_CREATED)
def subscribe_push(
    sub_in: PushSubscriptionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Saves or updates browser Web Push Subscription for the authenticated user.
    """
    existing = db.query(PushSubscription).filter(PushSubscription.endpoint == sub_in.endpoint).first()
    if existing:
        existing.user_id = current_user.id
        existing.p256dh = sub_in.keys.p256dh
        existing.auth = sub_in.keys.auth
        db.commit()
        db.refresh(existing)
        return existing

    new_sub = PushSubscription(
        user_id=current_user.id,
        endpoint=sub_in.endpoint,
        p256dh=sub_in.keys.p256dh,
        auth=sub_in.keys.auth
    )
    db.add(new_sub)
    db.commit()
    db.refresh(new_sub)
    return new_sub


@router.post("/test-sentinel")
async def test_sentinel_push(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Triggers the Modo Sentinela to test native Web Push Notification on localhost!
    """
    result = await run_sentinel_analysis_for_user(current_user, db)
    return {
        "message": "Teste do Modo Sentinela executado com sucesso!",
        "result": result
    }
