from typing import Optional
from pydantic import BaseModel


class CheckoutSessionResponse(BaseModel):
    checkout_url: str
    session_id: str


class SubscriptionStatusResponse(BaseModel):
    is_pro: bool
    stripe_customer_id: Optional[str] = None
    stripe_subscription_id: Optional[str] = None
