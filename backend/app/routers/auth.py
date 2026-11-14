from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from datetime import timedelta, datetime
import secrets

from app.db import get_db, UserModel
from app.auth import (
    get_user_by_email, create_user, verify_password,
    create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, get_current_user, hash_password
)
from app.services.audit import log_action
from app.services.email import send_brief_email

router = APIRouter()

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    full_name: str = ""

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    email: str
    full_name: str

class PasswordResetRequest(BaseModel):
    email: EmailStr

class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str

@router.post("/register", response_model=TokenResponse)
def register(body: RegisterRequest, db: Session = Depends(get_db)):
    existing = get_user_by_email(db, body.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    if len(body.password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters")
    user = create_user(db, body.email, body.password, body.full_name)
    log_action("user_registered", f"User {user.email} registered", user_email=user.email)
    token = create_access_token(
        data={"sub": user.email},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return TokenResponse(access_token=token, email=user.email, full_name=user.full_name or "")

@router.post("/login", response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = get_user_by_email(db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    if not user.is_active:
        raise HTTPException(status_code=401, detail="Account inactive")
    log_action("user_login", f"User {user.email} logged in", user_email=user.email)
    token = create_access_token(
        data={"sub": user.email},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return TokenResponse(access_token=token, email=user.email, full_name=user.full_name or "")

@router.get("/me")
def me(auth=Depends(get_current_user)):
    if auth["type"] != "user":
        raise HTTPException(status_code=400, detail="This endpoint requires user login")
    user = auth["user"]
    return {
        "id": user.id,
        "email": user.email,
        "full_name": user.full_name,
        "is_active": user.is_active
    }

@router.post("/password-reset/request")
async def request_password_reset(body: PasswordResetRequest, db: Session = Depends(get_db)):
    user = get_user_by_email(db, body.email)
    # Always return success to avoid email enumeration
    if user:
        token = secrets.token_urlsafe(32)
        user.reset_token = token
        user.reset_token_expires = datetime.utcnow() + timedelta(hours=1)
        db.commit()
        # In production send a real email with a link containing the token
        reset_link = f"http://localhost:5173/reset-password?token={token}"
        text = f"Password reset requested.\n\nUse this token or open the link:\n{reset_link}\n\nToken: {token}\n\nThis link expires in 1 hour."
        await send_brief_email([user.email], "FocalPoint Password Reset", text, None)
        log_action("password_reset_requested", f"Reset requested for {user.email}", user_email=user.email)
    return {"message": "If the email exists, a reset link has been sent."}

@router.post("/password-reset/confirm")
def confirm_password_reset(body: PasswordResetConfirm, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.reset_token == body.token).first()
    if not user or not user.reset_token_expires or user.reset_token_expires < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Invalid or expired reset token")
    if len(body.new_password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters")
    user.hashed_password = hash_password(body.new_password)
    user.reset_token = None
    user.reset_token_expires = None
    db.commit()
    log_action("password_reset_completed", f"Password reset for {user.email}", user_email=user.email)
    return {"message": "Password updated successfully. You can now log in."}
