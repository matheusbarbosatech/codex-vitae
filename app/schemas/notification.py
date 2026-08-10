import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, ConfigDict


class PushKeys(BaseModel):
    p256dh: str
    auth: str


class PushSubscriptionCreate(BaseModel):
    endpoint: str
    keys: PushKeys


class PushSubscriptionResponse(BaseModel):
    id: int
    user_id: int
    endpoint: str
    p256dh: str
    auth: str
    created_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)


class NotificationPayload(BaseModel):
    title: str
    body: str
    icon: Optional[str] = "/static/img/icon-192.png"
    url: Optional[str] = "/dashboard"
    data: Optional[Dict[str, Any]] = None


class VapidKeyResponse(BaseModel):
    public_key: str
