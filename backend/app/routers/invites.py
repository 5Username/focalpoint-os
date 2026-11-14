from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from datetime import datetime, timedelta
import secrets
import uuid

from app.db import SessionLocal, InviteModel, WorkspaceModel, WorkspaceMemberModel
from app.auth import get_current_user, require_verified_user
from app.services.audit import log_action
from app.services.email import send_brief_email
from app.services.rbac import require_roles

router = APIRouter()

class InviteCreate(BaseModel):
    email: EmailStr
    role: str = "member"  # member | admin | viewer

class InviteAccept(BaseModel):
    token: str

@router.post("/workspaces/{ws_id}/invites")
async def create_invite(ws_id: str, body: InviteCreate, auth=Depends(require_verified_user)):
    """Only owner or admin can create invites."""
    if body.role not in ("admin", "member", "viewer"):
        body.role = "member"

    if auth["type"] == "user":
        # Stricter RBAC: only owner/admin may invite
        require_roles(ws_id, auth["user"].email, ["owner", "admin"])

    db = SessionLocal()
    try:
        ws = db.query(WorkspaceModel).filter(WorkspaceModel.id == ws_id).first()
        if not ws:
            raise HTTPException(status_code=404, detail="Workspace not found")

        token = secrets.token_urlsafe(24)
        invite = InviteModel(
            id=str(uuid.uuid4())[:8],
            workspace_id=ws_id,
            email=body.email.lower(),
            role=body.role,
            token=token,
            invited_by=auth["user"].email if auth["type"] == "user" else "api",
            expires_at=datetime.utcnow() + timedelta(days=7)
        )
        db.add(invite)
        db.commit()

        invite_link = f"http://localhost:5173/accept-invite?token={token}"
        text = (
            f"You have been invited to join the workspace '{ws.name}' on FocalPoint OS.\n\n"
            f"Role: {body.role}\n\n"
            f"Accept the invite here:\n{invite_link}\n\n"
            f"Or use token: {token}\n\nThis invite expires in 7 days."
        )
        await send_brief_email([body.email], f"Invitation to {ws.name} on FocalPoint", text, None)

        log_action(
            "invite_created",
            f"Invited {body.email} as {body.role}",
            workspace_id=ws_id,
            user_email=auth["user"].email if auth["type"] == "user" else "api"
        )

        return {
            "id": invite.id,
            "email": invite.email,
            "role": invite.role,
            "token": token,
            "invite_link": invite_link,
            "expires_at": invite.expires_at.isoformat() + "Z"
        }
    finally:
        db.close()

@router.post("/accept")
def accept_invite(body: InviteAccept, auth=Depends(get_current_user)):
    if auth["type"] != "user":
        raise HTTPException(status_code=400, detail="You must be logged in to accept an invite")

    user = auth["user"]
    db = SessionLocal()
    try:
        invite = db.query(InviteModel).filter(InviteModel.token == body.token).first()
        if not invite:
            raise HTTPException(status_code=400, detail="Invalid invite token")
        if invite.accepted:
            raise HTTPException(status_code=400, detail="Invite already accepted")
        if invite.expires_at and invite.expires_at < datetime.utcnow():
            raise HTTPException(status_code=400, detail="Invite has expired")

        member = WorkspaceMemberModel(
            id=str(uuid.uuid4())[:8],
            workspace_id=invite.workspace_id,
            user_id=user.id,
            email=user.email,
            role=invite.role
        )
        db.add(member)
        invite.accepted = True
        db.commit()

        log_action(
            "invite_accepted",
            f"{user.email} joined as {invite.role}",
            workspace_id=invite.workspace_id,
            user_email=user.email
        )

        return {
            "message": "Invite accepted successfully",
            "workspace_id": invite.workspace_id,
            "role": invite.role
        }
    finally:
        db.close()

@router.get("/workspaces/{ws_id}/invites")
def list_invites(ws_id: str, auth=Depends(get_current_user)):
    if auth["type"] == "user":
        # Only owner/admin can list invites
        require_roles(ws_id, auth["user"].email, ["owner", "admin"])

    db = SessionLocal()
    try:
        rows = db.query(InviteModel).filter(InviteModel.workspace_id == ws_id).all()
        return [
            {
                "id": r.id,
                "email": r.email,
                "role": r.role,
                "accepted": r.accepted,
                "expires_at": r.expires_at.isoformat() + "Z" if r.expires_at else None,
                "created_at": r.created_at.isoformat() + "Z" if r.created_at else None
            }
            for r in rows
        ]
    finally:
        db.close()
