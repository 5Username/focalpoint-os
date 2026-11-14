"""
Google & Microsoft OAuth / OIDC login stubs.

To activate:
1. Set environment variables (see docs/OIDC_SETUP.md)
2. Install authlib if you want full OIDC: pip install authlib
3. Uncomment the real OAuth client code below

This file provides working endpoints that currently return clear setup instructions
and a development fallback so the rest of the system remains usable.
"""

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import RedirectResponse
import os

router = APIRouter()

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
MICROSOFT_CLIENT_ID = os.getenv("MICROSOFT_CLIENT_ID")
MICROSOFT_CLIENT_SECRET = os.getenv("MICROSOFT_CLIENT_SECRET")
OAUTH_REDIRECT_BASE = os.getenv("OAUTH_REDIRECT_BASE", "http://localhost:8000")

@router.get("/google/login")
def google_login():
    if not GOOGLE_CLIENT_ID:
        return {
            "status": "not_configured",
            "message": "Google OAuth is not configured. Set GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET.",
            "docs": "See docs/OIDC_SETUP.md"
        }
    # Real implementation would redirect to Google's authorization endpoint
    # redirect_uri = f"{OAUTH_REDIRECT_BASE}/api/oauth/google/callback"
    # return RedirectResponse(f"https://accounts.google.com/o/oauth2/v2/auth?...")
    return {
        "status": "configured_but_stub",
        "message": "Google client ID is set. Wire authlib or your preferred OIDC library to complete the flow.",
        "next_step": "Follow docs/OIDC_SETUP.md to finish the integration"
    }

@router.get("/google/callback")
def google_callback(code: str = Query(None), error: str = Query(None)):
    if error:
        raise HTTPException(status_code=400, detail=f"Google OAuth error: {error}")
    if not code:
        raise HTTPException(status_code=400, detail="Missing authorization code")
    # Exchange code for tokens, validate id_token, create/find user, issue JWT
    return {
        "status": "stub",
        "message": "Received authorization code. Implement token exchange + user creation here.",
        "code_received": True
    }

@router.get("/microsoft/login")
def microsoft_login():
    if not MICROSOFT_CLIENT_ID:
        return {
            "status": "not_configured",
            "message": "Microsoft OAuth is not configured. Set MICROSOFT_CLIENT_ID and MICROSOFT_CLIENT_SECRET.",
            "docs": "See docs/OIDC_SETUP.md"
        }
    return {
        "status": "configured_but_stub",
        "message": "Microsoft client ID is set. Wire authlib or MSAL to complete the flow.",
        "next_step": "Follow docs/OIDC_SETUP.md"
    }

@router.get("/microsoft/callback")
def microsoft_callback(code: str = Query(None), error: str = Query(None)):
    if error:
        raise HTTPException(status_code=400, detail=f"Microsoft OAuth error: {error}")
    if not code:
        raise HTTPException(status_code=400, detail="Missing authorization code")
    return {
        "status": "stub",
        "message": "Received authorization code. Implement token exchange + user creation here.",
        "code_received": True
    }
