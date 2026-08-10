from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.growth import BurnoutAuditRequest, BurnoutAuditResponse
from app.services.growth_service import generate_burnout_audit

router = APIRouter(prefix="/growth", tags=["Growth & Lead Magnets"])


@router.post("/burnout-audit", response_model=BurnoutAuditResponse, status_code=status.HTTP_201_CREATED)
def run_burnout_audit(req: BurnoutAuditRequest, db: Session = Depends(get_db)):
    """
    Public Lead Magnet: Auditor de Burnout Biométrico.
    Calculates burnout risk score and generates actionable report for visitors.
    """
    return generate_burnout_audit(req, db)
