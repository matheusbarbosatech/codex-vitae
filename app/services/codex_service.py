import hashlib
import datetime
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.user import User, CodexPlan, BiometricLog, DunbarContact, UlyssesContract
from app.core.llm_client import generate_codex_plan, MODULE_PROMPTS
from app.schemas.codex import (
    CodexModuleOverview,
    BiometricCalibrationResponse,
    ResonanceBiofeedbackResponse,
    NLPSemanticAuditResponse,
    DunbarAnalysisResponse,
    DecisionFatigueResponse,
    ChaosSimulationResponse,
    MementoMoriResponse
)
from app.services.terra_service import ingest_user_biometrics

# Metadata for the 6 Codex Vitae modules
CODEX_MODULES_CATALOG: List[Dict[str, Any]] = [
    {
        "key": "maquina",
        "title": "A Máquina",
        "subtitle": "Hardware Biológico & Biometria",
        "description": "Calibração biométrica de 480nm, biofeedback de ressonância 5.5bpm e otimização do ritmo circadiano.",
        "icon": "fa-dna",
        "focus_areas": ["Calibração Fótica 480nm", "Biofeedback 5.5 bpm", "rMSSD HRV", "Nadir Térmico"]
    },
    {
        "key": "processador",
        "title": "O Processador",
        "subtitle": "Software Cognitivo & NLP Socrático",
        "description": "Auditoria semântica via NLP, detecção de catastrofização, TCC socrático e desativação da rede DMN.",
        "icon": "fa-brain",
        "focus_areas": ["Auditoria Semântica NLP", "Questionamento Socrático", "Desativação DMN", "TCC Preditivo"]
    },
    {
        "key": "tribo",
        "title": "A Tribo",
        "subtitle": "Protocolos de Rede & Análise de Dunbar",
        "description": "Mapeamento fractal de Dunbar (camadas 5, 15, 50, 150), poda social e boosters de ocitocina endógena.",
        "icon": "fa-people-group",
        "focus_areas": ["Análise Fractal 5/15/50/150", "Social Pruning", "Score Ocitocina", "CRM de Confiança"]
    },
    {
        "key": "combustivel",
        "title": "O Combustível",
        "subtitle": "Fadiga de Decisão & Contratos de Ulisses",
        "description": "Rastreio de atrito, previsão de fadiga de decisão, Choiceless Architecture e Contratos Criptográficos.",
        "icon": "fa-bolt",
        "focus_areas": ["Rastreio de Atrito", "Choiceless Architecture", "Contratos de Ulisses SHA256", "Fadiga de Decisão"]
    },
    {
        "key": "escudo",
        "title": "O Escudo",
        "subtitle": "Simulador do Caos & Filtro de Epicteto",
        "description": "Simulação Virtual de Crises (Premeditatio Malorum) e Filtro Binário de Controle (Ruído vs Movimento).",
        "icon": "fa-shield-halved",
        "focus_areas": ["Premeditatio Malorum", "Filtro Binário de Epicteto", "Resiliência Dicotômica", "Inoculação do Estresse"]
    },
    {
        "key": "bussola",
        "title": "A Bússola",
        "subtitle": "Logoterapia & Memento Mori Biométrico",
        "description": "Profiling Lexical Axiológico, alinhamento de tarefas com valores e relógio de regressão Memento Mori.",
        "icon": "fa-compass",
        "focus_areas": ["Profiling Axiológico", "Logoterapia de Frankl", "Memento Mori Biométrico", "Legado Vital"]
    }
]


def get_all_modules() -> List[CodexModuleOverview]:
    return [CodexModuleOverview(**m) for m in CODEX_MODULES_CATALOG]


# 1. ALGORITMO MÓDULO 1: CALIBRAÇÃO BIOMÉTRICA & BIOFEEDBACK 5.5 BPM
async def calibrate_biometrics_module1(user: User, db: Session) -> BiometricCalibrationResponse:
    latest_bio = db.query(BiometricLog).filter(BiometricLog.user_id == user.id).order_by(BiometricLog.timestamp.desc()).first()
    if not latest_bio:
        latest_bio = await ingest_user_biometrics(user, db)

    hrv = latest_bio.hrv_rmssd or 50.0
    parasympathetic_exhaustion = hrv < 42.0

    # Photonic 480nm light timing prescription based on HRV & circadian nadir
    if parasympathetic_exhaustion:
        light_min = 30
        timing_str = "06:45 - 07:15 (Janela de Recalibração do Nadir Térmico)"
        hrv_status = "Esgotamento Parassimpático Detectado (rMSSD < 42ms)"
    else:
        light_min = 20
        timing_str = "07:00 - 07:20 (Janela Padrão de Avanço de Fase SCN)"
        hrv_status = "Homeostase Parassimpática Estável (rMSSD Ótimo)"

    return BiometricCalibrationResponse(
        hrv_status=hrv_status,
        parasympathetic_exhaustion=parasympathetic_exhaustion,
        recommended_light_exposure_min=light_min,
        light_timing=timing_str,
        trigger_resonance_biofeedback=parasympathetic_exhaustion
    )


def execute_resonance_biofeedback(user: User, duration_seconds: int = 180) -> ResonanceBiofeedbackResponse:
    # 5.5 cycles per minute -> 10.9 seconds per cycle (Inhale 5s, Exhale 5.9s)
    cycles = int((duration_seconds / 60.0) * 5.5)
    vagustone_gain = round(cycles * 1.45, 1)

    return ResonanceBiofeedbackResponse(
        cycles_completed=cycles,
        vagustone_increase_pct=vagustone_gain,
        session_status="Sincronização Autonômica Concluída. Tônus Vagal Reestabelecido."
    )


# 2. ALGORITMO MÓDULO 2: NLP SEMANTIC AUDIT & SOCRATIC CBT
def run_nlp_semantic_audit(journal_text: str) -> NLPSemanticAuditResponse:
    text_lower = journal_text.lower()
    distortions = []
    
    # Detect Catastrophizing
    if any(w in text_lower for w in ["tudo deu errado", "horrível", "desastre", "insuportável", "nunca", "destruiu"]):
        distortions.append("Catastrofização e Amplificação de Ameaça")
    
    # Detect Absolutist thinking
    if any(w in text_lower for w in ["sempre", "impossível", "ninguém", "obrigado a", "tenho que"]):
        distortions.append("Pensamento Absolutista/Tudo-ou-Nada")
    
    if not distortions:
        distortions.append("Tendência a Viés de Confirmação Negativo")

    dmn_index = min(100.0, float(len(distortions) * 42.5 + len(journal_text) * 0.05))

    socratic_questions = [
        "1. Qual é a evidência concreta e objetiva que comprova que este pensamento é 100% verdadeiro?",
        "2. Se o pior cenário hipotético ocorrer, quais são os 3 passos práticos para neutralizá-lo?",
        "3. Como Epicteto reinterpretaria esta situação focando apenas nas variáveis sob seu comando?"
    ]

    return NLPSemanticAuditResponse(
        detected_distortions=distortions,
        dmn_hyperactivity_index=round(dmn_index, 1),
        socratic_questions=socratic_questions
    )


# 3. ALGORITMO MÓDULO 3: DUNBAR FRACTAL ANALYSIS & OXYTOCIN BOOSTERS
def analyze_dunbar_network(user: User, db: Session) -> DunbarAnalysisResponse:
    contacts = db.query(DunbarContact).filter(DunbarContact.user_id == user.id).all()
    
    summary = {5: 0, 15: 0, 50: 0, 150: 0}
    pruning = []
    oxytocin = []

    for c in contacts:
        if c.dunbar_layer in summary:
            summary[c.dunbar_layer] += 1

        if c.is_toxic_friction:
            pruning.append(f"Social Pruning recomendado: Reduzir atrito com '{c.contact_name}' (Camada {c.dunbar_layer}).")
        elif c.dunbar_layer == 5 and c.oxytocin_impact_score >= 70:
            oxytocin.append(f"Ativar micro-ação de gratidão com '{c.contact_name}' (Camada 5 - Núcleo de Confiança).")

    if not pruning:
        pruning.append("Nenhum atrito tóxico detectado na sua rede atual.")
    if not oxytocin:
        oxytocin.append("Agende um contato de escuta ativa de 10 minutos com alguém do seu círculo interno (Camada 5).")

    return DunbarAnalysisResponse(
        layers_summary=summary,
        social_pruning_suggestions=pruning,
        oxytocin_boosters=oxytocin
    )


# 4. ALGORITMO MÓDULO 4: DECISION FATIGUE & ULYSSES CONTRACTS
def calculate_decision_fatigue(user: User, db: Session) -> DecisionFatigueResponse:
    # Check current time & biometric logs
    current_hour = datetime.datetime.utcnow().hour
    active_contracts = db.query(UlyssesContract).filter(UlyssesContract.user_id == user.id, UlyssesContract.is_active == True).count()

    if current_hour >= 18 or active_contracts >= 2:
        fatigue = "Critical"
        score = 28.5
        activate_choice = True
        hidden_count = 5
    else:
        fatigue = "Low"
        score = 88.0
        activate_choice = False
        hidden_count = 0

    return DecisionFatigueResponse(
        fatigue_level=fatigue,
        decision_capacity_score=score,
        activate_choiceless_architecture=activate_choice,
        hidden_stimuli_count=hidden_count
    )


def create_cryptographic_ulysses_contract(user: User, contract_in: Any, db: Session) -> UlyssesContract:
    raw_str = f"{user.id}:{contract_in.contract_title}:{datetime.datetime.utcnow().isoformat()}"
    crypto_sig = hashlib.sha256(raw_str.encode('utf-8')).hexdigest()

    contract = UlyssesContract(
        user_id=user.id,
        contract_title=contract_in.contract_title,
        commitment_details=contract_in.commitment_details,
        crypto_signature=crypto_sig,
        penalty_financial_cents=contract_in.penalty_financial_cents,
        is_active=True
    )
    db.add(contract)
    db.commit()
    db.refresh(contract)
    return contract


# 5. ALGORITMO MÓDULO 5: VIRTUAL CHAOS SIMULATOR & EPICTETUS FILTER
def run_virtual_chaos_simulation(upcoming_event: str) -> ChaosSimulationResponse:
    catastrophic = f"Simulação de Colapso: Falha completa em '{upcoming_event}' por imprevisto técnico/exógeno."
    
    steps = [
        "1. Visualizar o pior cenário possível em detalhes por 60 segundos (Premeditatio Malorum).",
        "2. Reconhecer que o pânico amigdaliano antecipado dessensibiliza o pico de cortisol real.",
        "3. Executar o plano de contingência imediato sem hesitação cognitiva."
    ]

    binary_filter = {
        "external_noise": [
            "Reação ou opinião de terceiros",
            "Atrasos de fornecedores/plataformas",
            "Instabilidade de mercado exógena"
        ],
        "movement_matrix": [
            "Sua postura e resposta emocional imediata",
            "Clareza do plano de contingência B",
            "Foco 100% no próximo passo sob seu comando"
        ]
    }

    return ChaosSimulationResponse(
        catastrophic_scenario=catastrophic,
        premeditatio_malorum_steps=steps,
        binary_control_filter=binary_filter
    )


# 6. ALGORITMO MÓDULO 6: LOGOTHERAPY & BIOMETRIC MEMENTO MORI
def calculate_biometric_memento_mori(user: User, user_age: int = 30) -> MementoMoriResponse:
    expected_life = 82.5
    years_left = max(1.0, expected_life - user_age)
    weeks_left = int(years_left * 52)
    days_left = int(years_left * 365)

    return MementoMoriResponse(
        age=user_age,
        estimated_lifespan_years=expected_life,
        years_remaining=round(years_left, 1),
        weeks_remaining=weeks_left,
        days_remaining=days_left,
        logotherapy_alignment_score=84.5,
        axiological_values=["Autenticidade", "Excelência Técnica", "Contribuição Social", "Resiliência Estoica"]
    )


# Standard plan creation
async def create_user_codex_plan(
    user: User,
    module_key: str,
    user_context: Optional[str],
    db: Session
) -> CodexPlan:
    if module_key not in MODULE_PROMPTS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Módulo '{module_key}' não existe no Codex Vitae."
        )

    # Check Reverse Trial & Pro status
    if not user.is_pro:
        user_plan_count = db.query(CodexPlan).filter(CodexPlan.user_id == user.id).count()
        if user_plan_count >= 3:
            raise HTTPException(
                status_code=status.HTTP_402_PAYMENT_REQUIRED,
                detail="Seu período de Reverse Trial encerrou e o limite do Plano Free foi atingido. Faça upgrade para o Plano PRO para desbloquear os 6 Módulos!"
            )

    mod_info = MODULE_PROMPTS[module_key]
    plan_output = await generate_codex_plan(module_key, user_context)

    new_plan = CodexPlan(
        user_id=user.id,
        module_key=module_key,
        module_title=mod_info["title"],
        input_data=user_context or "",
        plan_output=plan_output
    )

    db.add(new_plan)
    db.commit()
    db.refresh(new_plan)

    return new_plan


def get_user_plans(user: User, db: Session) -> List[CodexPlan]:
    return db.query(CodexPlan).filter(CodexPlan.user_id == user.id).order_by(CodexPlan.created_at.desc()).all()
