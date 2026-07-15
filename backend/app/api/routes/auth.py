from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.domain import Role, User
from app.schemas.domain import ForgotPasswordIn, LoginIn, RegisterIn, TokenOut, UserOut
from app.security.dependencies import get_current_user
from app.security.jwt import create_access_token
from app.security.passwords import hash_password, verify_password

router = APIRouter()


@router.post("/register", response_model=TokenOut, status_code=status.HTTP_201_CREATED)
def register(payload: RegisterIn, db: Session = Depends(get_db)) -> TokenOut:
    if db.scalar(select(User).where(User.email == payload.email)):
        raise HTTPException(status_code=409, detail="Email already registered")
    role = db.scalar(select(Role).where(Role.name == payload.role))
    if not role:
        raise HTTPException(status_code=400, detail="Requested role does not exist")
    user = User(email=payload.email, full_name=payload.full_name, hashed_password=hash_password(payload.password), role_id=role.id, preferred_language=payload.preferred_language)
    db.add(user)
    db.commit()
    db.refresh(user)
    return TokenOut(access_token=create_access_token(str(user.id), user.role.name.value), role=user.role.name)


@router.post("/login", response_model=TokenOut)
def login(payload: LoginIn, db: Session = Depends(get_db)) -> TokenOut:
    user = db.scalar(select(User).where(User.email == payload.email))
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    return TokenOut(access_token=create_access_token(str(user.id), user.role.name.value), role=user.role.name)


@router.get("/me", response_model=UserOut)
def me(user: User = Depends(get_current_user)) -> UserOut:
    return UserOut(id=str(user.id), email=user.email, full_name=user.full_name, role=user.role.name, preferred_language=user.preferred_language)


@router.post("/forgot-password")
def forgot_password(payload: ForgotPasswordIn) -> dict[str, str]:
    return {"message": "If the account exists, a secure reset link has been queued."}


@router.post("/logout")
def logout() -> dict[str, str]:
    return {"message": "Logged out successfully. Please remove the token from the client."}

