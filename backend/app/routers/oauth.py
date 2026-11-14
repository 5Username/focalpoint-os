"""
Real Google OAuth / OIDC login using authlib.
Microsoft remains a documented stub until credentials are provided.
"""

from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from datetime import timedelta
import os
import secrets

from app.db import get_db, UserModel
from app.auth import create_access_token, get_user_by_email, hash_password, ACCESS_TOKEN_EXPIRE_MINUTES
from app.services.audit import log_action

router = APIRouter()

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
OAUTH_REDIRECT_BASE = os.getenv("OAUTH_REDIRECT_BASE", "http://localhost:8000")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")

# authlib is optional at import time so the app still starts without it configured
try:
    from authlib.integrations.starlette_client import OAuth
    from starlette.config import Config

    config = Config(environ=os.environ)
    oauth = OAuth(config)

    if GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET:
        oauth.register(
            name="google",
            client_id=GOOGLE_CLIENT_ID,
            client_secret=GOOGLE_CLIENT_SECRET,
            server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
            client_kwargs={"scope": "openid email profile"},
        )
        GOOGLE_READY = True
    else:
        GOOGLE_READY = False
except Exception:
    oauth = None
    GOOGLE_READY = False


@router.get("/google/login")
async def google_login(request: Request):
    if not GOOGLE_READY or oauth is None:
        return {
            "status": "not_configured",
            "message": "Google OAuth is not configured. Set GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET.",
            "docs": "See docs/OIDC_SETUP.md"
        }
    redirect_uri = f"{OAUTH_REDIRECT_BASE}/api/oauth/google/callback"
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get("/google/callback")
async def google_callback(request: Request, db: Session = Depends(get_db)):
    if not GOOGLE_READY or oauth is None:
        raise HTTPException(status_code=400, detail="Google OAuth not configured")

    try:
        token = await oauth.google.authorize_access_token(request)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"OAuth failed: {e}")

    userinfo = token.get("userinfo")
    if not userinfo:
        # Fallback: parse id_token if userinfo not present
        userinfo = token.get("id_token") or {}

    email = userinfo.get("email")
    if not email:
        raise HTTPException(status_code=400, detail="Google account did not return an email")

    email_verified = userinfo.get("email_verified", True)
    full_name = userinfo.get("name") or userinfo.get("given_name") or ""

    # Find or create local user
    user = get_user_by_email(db, email)
    if not user:
        # Create with a random unusable password (SSO-only account)
        random_password = secrets.token_urlsafe(32)
        from app.auth import create_user
        user = create_user(db, email, random_password, full_name)

    # Mark verified because Google already verified the email
    if email_verified and not user.is_verified:
        user.is_verified = True
        user.verification_token = None
        db.commit()

    log_action("oauth_login_google", f"Google login for {email}", user_email=email)

    # Issue the same JWT used by the rest of the system
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    # Redirect to frontend with token (frontend should store it)
    redirect_url = f"{FRONTEND_URL}/oauth/callback?token={access_token}&email={user.email}&full_name={full_name or ''}"
    return RedirectResponse(redirect_url)


@router.get("/microsoft/login")
def microsoft_login():
    return {
        "status": "not_configured",
        "message": "Microsoft OAuth stub. Follow docs/OIDC_SETUP.md to enable it the same way as Google.",
        "docs": "docs/OIDC_SETUP.md"
    }
