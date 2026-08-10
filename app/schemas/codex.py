import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, ConfigDict


class CodexModuleRequest(BaseModel):
    module_key: str  # maquina, processador, tribo, combustivel, escudo, bussola
    user_context: Optional[str] = None
    age: Optional[int] = None
    main_goal: Optional[str] = None


class CodexPlanResponse(BaseModel):
    id: int
    module_key: str
    module_title: str
    input_data: Optional[str] = None
    plan_output: str
    created_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)


class CodexModuleOverview(BaseModel):
    key: str
    title: str
    subtitle: str
    description: str
    icon: str
    focus_areas: List[str]


# Advanced Algorithm Schemas

class BiometricCalibrationResponse(BaseModel):
    hrv_status: str
    parasympathetic_exhaustion: bool
    recommended_light_exposure_min: int  # 480nm blue light exposure minutes
    light_timing: str
    trigger_resonance_biofeedback: bool  # 5.5 cycles/min breathing trigger


class ResonanceBiofeedbackRequest(BaseModel):
    duration_seconds: int = 180
    breathing_rate_bpm: float = 5.5  # 5.5 cycles per minute


class ResonanceBiofeedbackResponse(BaseModel):
    cycles_completed: int
    vagustone_increase_pct: float
    session_status: str


class NLPSemanticAuditRequest(BaseModel):
    journal_entry: str


class NLPSemanticAuditResponse(BaseModel):
    detected_distortions: List[str]  # e.g., 'catastrophizing', 'absolutist_thinking'
    dmn_hyperactivity_index: float
    socratic_questions: List[str]  # CBT questioning for DMN disengagement


class DunbarContactCreate(BaseModel):
    contact_name: str
    dunbar_layer: int  # 5, 15, 50, 150
    oxytocin_impact_score: float = 50.0
    is_toxic_friction: bool = False


class DunbarContactResponse(BaseModel):
    id: int
    contact_name: str
    dunbar_layer: int
    oxytocin_impact_score: float
    is_toxic_friction: bool
    last_interaction: datetime.datetime

    model_config = ConfigDict(from_attributes=True)


class DunbarAnalysisResponse(BaseModel):
    layers_summary: Dict[int, int]
    social_pruning_suggestions: List[str]
    oxytocin_boosters: List[str]


class UlyssesContractCreate(BaseModel):
    contract_title: str
    commitment_details: str
    penalty_financial_cents: int = 0


class UlyssesContractResponse(BaseModel):
    id: int
    contract_title: str
    commitment_details: str
    crypto_signature: str
    penalty_financial_cents: int
    is_active: bool
    created_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)


class DecisionFatigueResponse(BaseModel):
    fatigue_level: str  # 'Low', 'Moderate', 'Critical'
    decision_capacity_score: float
    activate_choiceless_architecture: bool
    hidden_stimuli_count: int


class ChaosSimulationRequest(BaseModel):
    upcoming_event: str


class ChaosSimulationResponse(BaseModel):
    catastrophic_scenario: str
    premeditatio_malorum_steps: List[str]
    binary_control_filter: Dict[str, List[str]]  # 'external_noise' vs 'movement_matrix'


class MementoMoriResponse(BaseModel):
    age: int
    estimated_lifespan_years: float
    years_remaining: float
    weeks_remaining: int
    days_remaining: int
    logotherapy_alignment_score: float
    axiological_values: List[str]
