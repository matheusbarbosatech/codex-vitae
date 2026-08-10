import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, ConfigDict


class TerraWebhookPayload(BaseModel):
    user_id: Optional[str] = None
    type: str  # 'sleep', 'daily', 'body'
    data: Dict[str, Any]


class BiometricIngestRequest(BaseModel):
    hrv_rmssd: float
    deep_sleep_minutes: int
    glucose_avg_mg_dl: Optional[float] = 95.0
    readiness_score: float


class BiometricLogResponse(BaseModel):
    id: int
    user_id: int
    hrv_rmssd: Optional[float]
    hf_hrv_power: Optional[float]
    deep_sleep_minutes: Optional[int]
    glucose_avg_mg_dl: Optional[float]
    readiness_score: Optional[float]
    allostatic_load_score: Optional[float]
    timestamp: datetime.datetime

    model_config = ConfigDict(from_attributes=True)
