import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Float, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    full_name = Column(String(255), nullable=True)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    is_pro = Column(Boolean, default=True)  # Reverse Trial: starts True for 14 days
    trial_ends_at = Column(DateTime, nullable=True)
    stripe_customer_id = Column(String(255), nullable=True, index=True)
    stripe_subscription_id = Column(String(255), nullable=True, index=True)
    cronotype_baseline = Column(String(50), default="Intermediate")
    memento_mori_years_left = Column(Float, default=45.0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    plans = relationship("CodexPlan", back_populates="owner", cascade="all, delete-orphan")
    biometrics = relationship("BiometricLog", back_populates="owner", cascade="all, delete-orphan")
    dunbar_contacts = relationship("DunbarContact", back_populates="owner", cascade="all, delete-orphan")
    ulysses_contracts = relationship("UlyssesContract", back_populates="owner", cascade="all, delete-orphan")
    push_subscriptions = relationship("PushSubscription", back_populates="owner", cascade="all, delete-orphan")


class CodexPlan(Base):
    __tablename__ = "codex_plans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    module_key = Column(String(50), nullable=False)
    module_title = Column(String(100), nullable=False)
    input_data = Column(Text, nullable=True)
    plan_output = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    owner = relationship("User", back_populates="plans")


class BiometricLog(Base):
    __tablename__ = "biometric_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    hrv_rmssd = Column(Float, nullable=True)
    hf_hrv_power = Column(Float, nullable=True)
    deep_sleep_minutes = Column(Integer, nullable=True)
    glucose_avg_mg_dl = Column(Float, nullable=True)
    readiness_score = Column(Float, nullable=True)
    allostatic_load_score = Column(Float, nullable=True)
    raw_payload = Column(JSON, nullable=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

    owner = relationship("User", back_populates="biometrics")


class DunbarContact(Base):
    __tablename__ = "dunbar_contacts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    contact_name = Column(String(255), nullable=False)
    dunbar_layer = Column(Integer, nullable=False)
    oxytocin_impact_score = Column(Float, default=50.0)
    is_toxic_friction = Column(Boolean, default=False)
    last_interaction = Column(DateTime, default=datetime.datetime.utcnow)

    owner = relationship("User", back_populates="dunbar_contacts")


class UlyssesContract(Base):
    __tablename__ = "ulysses_contracts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    contract_title = Column(String(255), nullable=False)
    commitment_details = Column(Text, nullable=False)
    crypto_signature = Column(String(64), nullable=False)
    penalty_financial_cents = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    owner = relationship("User", back_populates="ulysses_contracts")


class BurnoutAuditLog(Base):
    __tablename__ = "burnout_audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    lead_email = Column(String(255), index=True, nullable=False)
    burnout_risk_score = Column(Float, nullable=False)
    fatigue_index = Column(Float, nullable=False)
    recommended_module = Column(String(50), nullable=False)
    audit_report_data = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class PushSubscription(Base):
    __tablename__ = "push_subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    endpoint = Column(Text, nullable=False, unique=True, index=True)
    p256dh = Column(String(255), nullable=False)
    auth = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    owner = relationship("User", back_populates="push_subscriptions")
