import logging
import datetime
from typing import Optional, Dict, Any

try:
    import stripe
    STRIPE_AVAILABLE = True
except ImportError:
    stripe = None
    STRIPE_AVAILABLE = False

from app.core.config import settings
from app.models.user import User
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

if STRIPE_AVAILABLE and settings.STRIPE_SECRET_KEY:
    stripe.api_key = settings.STRIPE_SECRET_KEY


def check_and_update_user_trial_status(user: User, db: Session) -> User:
    """
    Reverse Trial Logic:
    - Every user gets 14 days of automatic Pro access upon registration.
    - If trial_ends_at is past and user has no active Stripe subscription, user drops to Free tier (is_pro = False).
    - Loss Aversion is triggered when falling to Free tier.
    """
    if user.stripe_subscription_id:
        # User has a paid Stripe subscription
        user.is_pro = True
        db.commit()
        return user

    if user.trial_ends_at:
        now = datetime.datetime.utcnow()
        if now > user.trial_ends_at:
            if user.is_pro:
                logger.info(f"Reverse Trial finalizado para {user.email}. Retirando privilégios PRO (Gatilho Loss Aversion).")
                user.is_pro = False
                db.commit()

    return user


def create_stripe_checkout_session(user: User) -> Dict[str, str]:
    """
    Creates a Stripe Checkout Session for Pro subscription upgrade.
    Falls back to a simulated checkout URL if STRIPE_SECRET_KEY is not set.
    """
    if not settings.STRIPE_SECRET_KEY:
        logger.info(f"Stripe API Key não configurada. Gerando sessão de checkout simulada para {user.email}.")
        mock_session_id = f"cs_test_mock_{user.id}_12345"
        mock_url = f"{settings.DOMAIN_URL}/dashboard?checkout_status=success_mock&session_id={mock_session_id}"
        return {"checkout_url": mock_url, "session_id": mock_session_id}

    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            customer_email=user.email,
            client_reference_id=str(user.id),
            line_items=[
                {
                    "price": settings.STRIPE_PRICE_ID_PRO,
                    "quantity": 1,
                },
            ],
            mode="subscription",
            success_url=f"{settings.DOMAIN_URL}/dashboard?checkout_status=success",
            cancel_url=f"{settings.DOMAIN_URL}/#pricing",
        )
        return {
            "checkout_url": checkout_session.url,
            "session_id": checkout_session.id
        }
    except Exception as e:
        logger.error(f"Erro ao criar sessão no Stripe: {e}")
        raise RuntimeError(f"Erro na integração Stripe: {str(e)}")


def handle_stripe_webhook(payload: bytes, sig_header: str, db: Session) -> bool:
    """
    Handles Stripe Webhook events to upgrade/downgrade user PRO status.
    """
    if not settings.STRIPE_SECRET_KEY or not settings.STRIPE_WEBHOOK_SECRET:
        logger.warning("Stripe Webhook Secret não configurado.")
        return False

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except Exception as e:
        logger.error(f"Assinatura do Webhook inválida: {e}")
        return False

    event_type = event["type"]
    data_object = event["data"]["object"]

    if event_type == "checkout.session.completed":
        user_id = data_object.get("client_reference_id")
        customer_id = data_object.get("customer")
        subscription_id = data_object.get("subscription")

        if user_id:
            user = db.query(User).filter(User.id == int(user_id)).first()
            if user:
                user.is_pro = True
                user.stripe_customer_id = customer_id
                user.stripe_subscription_id = subscription_id
                db.commit()
                logger.info(f"Usuário {user.email} atualizado para PRO com sucesso via Webhook.")

    elif event_type in ["customer.subscription.deleted", "customer.subscription.updated"]:
        subscription_id = data_object.get("id")
        status = data_object.get("status")
        
        user = db.query(User).filter(User.stripe_subscription_id == subscription_id).first()
        if user:
            if status in ["canceled", "unpaid"]:
                user.is_pro = False
                user.stripe_subscription_id = None
                db.commit()
                logger.info(f"Assinatura do usuário {user.email} cancelada/expirada.")
            elif status == "active":
                user.is_pro = True
                db.commit()

    return True
