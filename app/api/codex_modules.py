from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.core.security import get_current_user
from app.schemas.codex import (
    CodexModuleRequest,
    CodexPlanResponse,
    CodexModuleOverview,
    BiometricCalibrationResponse,
    ResonanceBiofeedbackRequest,
    ResonanceBiofeedbackResponse,
    NLPSemanticAuditRequest,
    NLPSemanticAuditResponse,
    DunbarContactCreate,
    DunbarContactResponse,
    DunbarAnalysisResponse,
    UlyssesContractCreate,
    UlyssesContractResponse,
    DecisionFatigueResponse,
    ChaosSimulationRequest,
    ChaosSimulationResponse,
    MementoMoriResponse
)
from app.services.codex_service import (
    get_all_modules,
    create_user_codex_plan,
    get_user_plans,
    calibrate_biometrics_module1,
    execute_resonance_biofeedback,
    run_nlp_semantic_audit,
    analyze_dunbar_network,
    calculate_decision_fatigue,
    create_cryptographic_ulysses_contract,
    run_virtual_chaos_simulation,
    calculate_biometric_memento_mori
)
from app.models.user import DunbarContact, UlyssesContract

router = APIRouter(prefix="/codex", tags=["Módulos do Codex Vitae"])


@router.get("/modules", response_model=List[CodexModuleOverview])
def list_modules():
    return get_all_modules()


@router.post("/generate", response_model=CodexPlanResponse, status_code=status.HTTP_201_CREATED)
async def generate_plan(
    req: CodexModuleRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    plan = await create_user_codex_plan(
        user=current_user,
        module_key=req.module_key,
        user_context=req.user_context,
        db=db
    )
    return plan


@router.get("/plans", response_model=List[CodexPlanResponse])
def list_user_plans(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_user_plans(current_user, db)


# MÓDULO 1: BIOMETRIA & BIOFEEDBACK DE RESSONÂNCIA (5.5 BPM)
@router.post("/module1/calibrate", response_model=BiometricCalibrationResponse)
async def calibrate_module1(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return await calibrate_biometrics_module1(current_user, db)


@router.post("/module1/resonance-biofeedback", response_model=ResonanceBiofeedbackResponse)
def biofeedback_module1(
    req: ResonanceBiofeedbackRequest,
    current_user: User = Depends(get_current_user)
):
    return execute_resonance_biofeedback(current_user, req.duration_seconds)


# MÓDULO 2: AUDITORIA SEMÂNTICA NLP & QUESTIONAMENTO SOCRÁTICO
@router.post("/module2/nlp-audit", response_model=NLPSemanticAuditResponse)
def nlp_audit_module2(
    req: NLPSemanticAuditRequest,
    current_user: User = Depends(get_current_user)
):
    return run_nlp_semantic_audit(req.journal_entry)


# MÓDULO 3: ANÁLISE FRACTAL DE DUNBAR & SOCIAL PRUNING
@router.get("/module3/dunbar", response_model=DunbarAnalysisResponse)
def dunbar_analysis_module3(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return analyze_dunbar_network(current_user, db)


@router.post("/module3/dunbar-contact", response_model=DunbarContactResponse, status_code=status.HTTP_201_CREATED)
def add_dunbar_contact(
    contact_in: DunbarContactCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    contact = DunbarContact(
        user_id=current_user.id,
        contact_name=contact_in.contact_name,
        dunbar_layer=contact_in.dunbar_layer,
        oxytocin_impact_score=contact_in.oxytocin_impact_score,
        is_toxic_friction=contact_in.is_toxic_friction
    )
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


# MÓDULO 4: FADIGA DE DECISÃO & CONTRATOS DE ULISSES (SHA256)
@router.get("/module4/decision-fatigue", response_model=DecisionFatigueResponse)
def decision_fatigue_module4(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return calculate_decision_fatigue(current_user, db)


@router.post("/module4/ulysses-contract", response_model=UlyssesContractResponse, status_code=status.HTTP_201_CREATED)
def ulysses_contract_module4(
    contract_in: UlyssesContractCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return create_cryptographic_ulysses_contract(current_user, contract_in, db)


# MÓDULO 5: SIMULADOR DO CAOS & FILTRO DE EPICTETO
@router.post("/module5/chaos-simulation", response_model=ChaosSimulationResponse)
def chaos_simulation_module5(
    req: ChaosSimulationRequest,
    current_user: User = Depends(get_current_user)
):
    return run_virtual_chaos_simulation(req.upcoming_event)


# MÓDULO 6: LOGOTERAPIA & MEMENTO MORI BIOMÉTRICO
@router.get("/module6/memento-mori", response_model=MementoMoriResponse)
def memento_mori_module6(
    current_user: User = Depends(get_current_user)
):
    return calculate_biometric_memento_mori(current_user)
