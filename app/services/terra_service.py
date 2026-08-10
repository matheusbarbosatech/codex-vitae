import logging
import random
import datetime
from typing import Dict, Any, Optional
import httpx
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.user import User, BiometricLog

logger = logging.getLogger(__name__)


def generate_mock_biometrics(user_id: int) -> Dict[str, Any]:
    """
    Generates realistic biometric telemetry data for Oura, Apple Health & Garmin mock ingestion.
    """
    hrv = random.uniform(35.0, 85.0)
    hf_hrv = hrv * random.uniform(0.8, 1.2)
    deep_sleep = random.randint(45, 110)
    glucose = random.uniform(85.0, 115.0)
    readiness = random.uniform(60.0, 95.0)
    allostatic_load = max(0.0, 100.0 - readiness + random.uniform(-5.0, 10.0))

    return {
        "user_id": user_id,
        "hrv_rmssd": round(hrv, 2),
        "hf_hrv_power": round(hf_hrv, 2),
        "deep_sleep_minutes": deep_sleep,
        "glucose_avg_mg_dl": round(glucose, 1),
        "readiness_score": round(readiness, 1),
        "allostatic_load_score": round(allostatic_load, 1),
        "raw_payload": {
            "source": "TerraAPI_MockAggregator",
            "devices": ["Oura_Ring_Gen3", "Apple_Watch_Ultra", "Dexcom_G7"],
            "timestamp": datetime.datetime.utcnow().isoformat()
        }
    }


async def ingest_user_biometrics(user: User, db: Session, custom_data: Optional[Dict[str, Any]] = None) -> BiometricLog:
    """
    Ingests biometric data from Terra API or mock generator and saves to database.
    """
    if custom_data:
        hrv = custom_data.get("hrv_rmssd", 55.0)
        hf_hrv = hrv * 0.9
        deep_sleep = custom_data.get("deep_sleep_minutes", 75)
        glucose = custom_data.get("glucose_avg_mg_dl", 95.0)
        readiness = custom_data.get("readiness_score", 80.0)
        allostatic_load = max(0.0, 100.0 - readiness)
        payload = custom_data
    elif settings.TERRA_API_KEY and settings.TERRA_DEV_ID:
        try:
            logger.info(f"Conectando à Terra API para usuário {user.email}...")
            # Example Terra API endpoint call
            async with httpx.AsyncClient() as client:
                resp = await client.get(
                    f"https://api.tryterra.co/v2/daily?user_id={user.email}",
                    headers={
                        "dev-id": settings.TERRA_DEV_ID,
                        "x-api-key": settings.TERRA_API_KEY
                    },
                    timeout=5.0
                )
                if resp.status_code == 200:
                    terra_json = resp.json()
                    # Parse data from Terra API
                    hrv = terra_json.get("data", [{}])[0].get("heart_rate_data", {}).get("summary", {}).get("avg_hrv_rmssd", 58.0)
                    hf_hrv = hrv * 0.95
                    deep_sleep = int(terra_json.get("data", [{}])[0].get("sleep_data", {}).get("deep_sleep_duration_seconds", 4500) / 60)
                    glucose = 92.0
                    readiness = 82.0
                    allostatic_load = 18.0
                    payload = terra_json
                else:
                    mock_b = generate_mock_biometrics(user.id)
                    return await ingest_user_biometrics(user, db, mock_b)
        except Exception as e:
            logger.warning(f"Erro ao conectar com Terra API ({e}). Usando gerador mock.")
            mock_b = generate_mock_biometrics(user.id)
            return await ingest_user_biometrics(user, db, mock_b)
    else:
        mock_b = generate_mock_biometrics(user.id)
        hrv = mock_b["hrv_rmssd"]
        hf_hrv = mock_b["hf_hrv_power"]
        deep_sleep = mock_b["deep_sleep_minutes"]
        glucose = mock_b["glucose_avg_mg_dl"]
        readiness = mock_b["readiness_score"]
        allostatic_load = mock_b["allostatic_load_score"]
        payload = mock_b["raw_payload"]

    log = BiometricLog(
        user_id=user.id,
        hrv_rmssd=hrv,
        hf_hrv_power=hf_hrv,
        deep_sleep_minutes=deep_sleep,
        glucose_avg_mg_dl=glucose,
        readiness_score=readiness,
        allostatic_load_score=allostatic_load,
        raw_payload=payload
    )

    db.add(log)
    db.commit()
    db.refresh(log)

    return log
