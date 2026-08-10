import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, EmailStr, ConfigDict


class BurnoutAuditRequest(BaseModel):
    email: EmailStr
    avg_sleep_hours: float
    perceived_stress_level: int  # 1 to 10
    weekly_work_hours: float
    reported_hrv: Optional[float] = None


class BurnoutAuditResponse(BaseModel):
    id: int
    lead_email: str
    burnout_risk_score: float
    fatigue_index: float
    recommended_module: str
    audit_report_data: Dict[str, Any]
    created_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)


class OnboardingRequest(BaseModel):
    primary_friction: str  # 'focus_dispersion', 'physical_exhaustion', 'anxiety'
    authorize_wearables: bool = True
    manual_hrv: Optional[float] = None


class OnboardingAhaResponse(BaseModel):
    message: str
    biometrics_imported_days: int
    cortisol_spike_risk_day: str
    reorganized_schedule: List[Dict[str, Any]]
    recommended_module: str
