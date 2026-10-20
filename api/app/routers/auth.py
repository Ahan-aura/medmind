from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.models import User
from app.schemas.auth import RegisterRequest, LoginRequest, AuthResponse, UserResponse
from app.security import hash_password, verify_password, create_access_token, get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=AuthResponse)
def register(req: RegisterRequest, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == req.email.lower()).first()
    if existing:
        raise HTTPException(status_code=400, detail="An account with this email already exists")
        
    user = User(
        email=req.email.lower(),
        password_hash=hash_password(req.password),
        display_name=req.display_name,
        role=req.role if req.role in ('student', 'teacher', 'admin') else 'student',
        preferred_lang=req.preferred_lang or 'en',
        cohort_id=req.cohort_id or "cohort-med-2026-alpha"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    token = create_access_token({"sub": user.id, "role": user.role})
    return AuthResponse(
        access_token=token,
        user=UserResponse(
            id=user.id,
            email=user.email,
            display_name=user.display_name,
            role=user.role,
            preferred_lang=user.preferred_lang,
            cohort_id=user.cohort_id
        )
    )

@router.post("/login", response_model=AuthResponse)
def login(req: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == req.email.lower()).first()
    if not user or not verify_password(req.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")
        
    token = create_access_token({"sub": user.id, "role": user.role})
    return AuthResponse(
        access_token=token,
        user=UserResponse(
            id=user.id,
            email=user.email,
            display_name=user.display_name,
            role=user.role,
            preferred_lang=user.preferred_lang,
            cohort_id=user.cohort_id
        )
    )

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        display_name=current_user.display_name,
        role=current_user.role,
        preferred_lang=current_user.preferred_lang,
        cohort_id=current_user.cohort_id
    )
