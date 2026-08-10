import os
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "Codex Vitae SaaS"
    VERSION: str = "2.1.0"
    API_V1_STR: str = "/api/v1"
    
    SECRET_KEY: str = "super-secret-jwt-key-change-in-production-12345"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 30  # 30 days
    
    DATABASE_URL: str = "sqlite:///./codex_vitae.db"
    
    # LLM Settings (LiteLLM with Cost Control Proxy & Fallbacks)
    GROQ_API_KEY: Optional[str] = None
    OPENROUTER_API_KEY: Optional[str] = None
    OPENAI_API_KEY: Optional[str] = None
    DEFAULT_LLM_MODEL: str = "groq/llama-3.3-70b-versatile"
    FAST_LLM_MODEL: str = "groq/llama-3.1-8b-instant"
    
    # VAPID Keys for PWA Native Push Notifications
    VAPID_PUBLIC_KEY: str = "BEl62iUYgUivxIkv69yViEuiBIa45xV8_7xJ0ElnX_E7f3Wv1Uu91Nf4-X2xY5f4y_uW0130X-w0"
    VAPID_PRIVATE_KEY: str = "mM8v-U0130X-w0_7xJ0ElnX_E7f3Wv1Uu91Nf4-X2xY"
    VAPID_CLAIM_EMAIL: str = "mailto:sentinel@codexvitae.io"
    
    # Celery & Worker Settings
    CELERY_BROKER_URL: str = "memory://"
    CELERY_RESULT_BACKEND: str = "rpc://"
    
    # Stripe Monetization & Reverse Trial Settings
    STRIPE_SECRET_KEY: Optional[str] = None
    STRIPE_PUBLISHABLE_KEY: Optional[str] = None
    STRIPE_WEBHOOK_SECRET: Optional[str] = None
    STRIPE_PRICE_ID_PRO: str = "price_pro_tier_codex"
    REVERSE_TRIAL_DAYS: int = 14
    DOMAIN_URL: str = "http://localhost:8000"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    @property
    def sync_database_url(self) -> str:
        """Fix postgres:// scheme from older PaaS defaults to postgresql://"""
        url = self.DATABASE_URL
        if url.startswith("postgres://"):
            url = url.replace("postgres://", "postgresql://", 1)
        return url


settings = Settings()
