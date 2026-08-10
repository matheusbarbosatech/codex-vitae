from fastapi import APIRouter, Depends, Request, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.core.security import get_current_user
from app.schemas.billing import CheckoutSessionResponse, SubscriptionStatusResponse
from app.services.stripe_service import create_stripe_checkout_session, handle_stripe_webhook

router = APIRouter(prefix="/billing", tags=["Monetização & Stripe"])


@router.post("/checkout", response_model=CheckoutSessionResponse)
def create_checkout(
    current_user: User = Depends(get_current_user)
):
    """
    Creates a Stripe Checkout session to upgrade user to Plano PRO.
    """
    try:
        session_data = create_stripe_checkout_session(current_user)
        return CheckoutSessionResponse(**session_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao processar checkout do Stripe: {str(e)}"
        )


@router.get("/status", response_model=SubscriptionStatusResponse)
def get_subscription_status(
    current_user: User = Depends(get_current_user)
):
    """Returns subscription status for current user"""
    return SubscriptionStatusResponse(
        is_pro=current_user.is_pro,
        stripe_customer_id=current_user.stripe_customer_id,
        stripe_subscription_id=current_user.stripe_subscription_id
    )


@router.post("/webhook")
async def stripe_webhook(request: Request, db: Session = Depends(get_db)):
    """
    Stripe Webhook listener endpoint
    """
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature", "")
    
    success = handle_stripe_webhook(payload, sig_header, db)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Falha ao validar webhook do Stripe."
        )
    return {"status": "success"}
