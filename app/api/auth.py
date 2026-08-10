import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, UserLogin
from app.schemas.token import Token
from app.schemas.growth import OnboardingRequest, OnboardingAhaResponse
from app.core.config import settings
from app.core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    get_current_user
)
from app.services.stripe_service import check_and_update_user_trial_status
from app.services.growth_service import execute_onboarding_aha_funnel

router = APIRouter(prefix="/auth", tags=["Autenticação & Reverse Trial"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_in: UserCreate, response: Response, db: Session = Depends(get_db)):
    """
    Register a new user in Codex Vitae.
    Reverse Trial PLG: Grants 14 days of automatic full PRO access!
    """
    existing_user = db.query(User).filter(User.email == user_in.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Este e-mail já está cadastrado no sistema."
        )

    trial_end = datetime.datetime.utcnow() + datetime.timedelta(days=settings.REVERSE_TRIAL_DAYS)
    hashed_pw = get_password_hash(user_in.password)
    
    new_user = User(
        email=user_in.email,
        full_name=user_in.full_name,
        hashed_password=hashed_pw,
        is_active=True,
        is_pro=True,  # 14 days Reverse Trial Pro
        trial_ends_at=trial_end
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    access_token = create_access_token(subject=new_user.id)
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        max_age=30 * 24 * 60 * 60,
        samesite="lax"
    )

    return new_user


@router.post("/login", response_model=Token)
def login(login_data: UserLogin, response: Response, db: Session = Depends(get_db)):
    """Login with JSON payload and check trial expiration"""
    user = db.query(User).filter(User.email == login_data.email).first()
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos."
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Esta conta está inativa."
        )

    # Check Reverse Trial status
    check_and_update_user_trial_status(user, db)

    access_token = create_access_token(subject=user.id)
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        max_age=30 * 24 * 60 * 60,
        samesite="lax"
    )

    return Token(access_token=access_token, token_type="bearer")


@router.post("/login/form", response_model=Token)
def login_form(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos."
        )

    check_and_update_user_trial_status(user, db)

    access_token = create_access_token(subject=user.id)
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        max_age=30 * 24 * 60 * 60,
        samesite="lax"
    )
    return Token(access_token=access_token, token_type="bearer")


@router.post("/onboarding", response_model=OnboardingAhaResponse)
async def complete_onboarding(
    req: OnboardingRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    5-Minute Aha Moment Onboarding Funnel:
    Connects wearables, ingests 14-day telemetry, reorganizes schedule.
    """
    res = await execute_onboarding_aha_funnel(current_user, req.primary_friction, db)
    return res


@router.post("/logout")
def logout(response: Response):
    response.delete_cookie("access_token")
    return {"message": "Sessão encerrada com sucesso."}


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    check_and_update_user_trial_status(current_user, db)
    return current_user
