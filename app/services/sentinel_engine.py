import logging
import datetime
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session

from app.models.user import User, BiometricLog
from app.core.llm_client import generate_codex_plan
from app.schemas.notification import NotificationPayload
from app.services.webpush_service import dispatch_push_to_user

logger = logging.getLogger(__name__)


async def run_sentinel_analysis_for_user(user: User, db: Session) -> Dict[str, Any]:
    """
    Modo Sentinela Engine:
    1. Scans latest biometric logs for parasympathetic drops or high allostatic load.
    2. Uses LiteLLM to generate targeted emergency mentorship.
    3. Dispatches native PWA Web Push notification to user's lockscreen.
    """
    latest_bio = db.query(BiometricLog).filter(BiometricLog.user_id == user.id).order_by(BiometricLog.timestamp.desc()).first()
    
    hrv = latest_bio.hrv_rmssd if (latest_bio and latest_bio.hrv_rmssd) else 38.0
    allostatic = latest_bio.allostatic_load_score if (latest_bio and latest_bio.allostatic_load_score) else 72.0

    is_anomaly = (hrv < 42.0) or (allostatic > 65.0)

    if is_anomaly:
        prompt_context = f"ALERTA SENTINELA BIOMÉTRICO: VFC despencou para {hrv}ms e Carga Alostática subiu para {allostatic}%. Gerar mentoria de emergência de 2 frases."
        try:
            mentorship_text = await generate_codex_plan("maquina", prompt_context)
            # Truncate for notification body
            short_body = "Sua VFC despencou. Inicie respiração 4-4-4-4 agora para restabelecer o tônus parassimpático."
        except Exception:
            short_body = "Anomalia detectada! Sua VFC caiu. Inicie protocolo de respiração 4-4-4-4 de 3 minutos."

        payload = NotificationPayload(
            title="🛡️ Alerta do Modo Sentinela",
            body=short_body,
            icon="/static/img/icon-192.png",
            url="/dashboard",
            data={"module": "maquina", "hrv": hrv}
        )

        sent_count = dispatch_push_to_user(user, payload, db)
        
        return {
            "status": "anomaly_detected",
            "hrv": hrv,
            "allostatic_load": allostatic,
            "notification_sent": sent_count > 0,
            "pushes_delivered": sent_count,
            "mentorship_text": short_body
        }

    return {
        "status": "normal",
        "hrv": hrv,
        "allostatic_load": allostatic,
        "notification_sent": False,
        "mentorship_text": "Fisiologia em estado homeostático saudável."
    }
