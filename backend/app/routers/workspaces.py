from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from app.services.workspaces import (
    create_workspace, get_workspace, list_workspaces,
    update_workspace, set_brief_schedule, add_member
)
from app.auth import require_verified_user, get_current_user
from app.scheduler import reload_schedules
from app.services.audit import log_action
from app.services.rbac import require_roles

router = APIRouter()

class WorkspaceCreate(BaseModel):
    name: str
    region: str = "Kenya"
    primary_language: str = "en"
    owner_email: Optional[EmailStr] = None

class WorkspaceUpdate(BaseModel):
    name: Optional[str] = None
    region: Optional[str] = None
    primary_language: Optional[str] = None
    notify_emails: Optional[List[str]] = None

class ScheduleConfig(BaseModel):
    day_of_week: str = "monday"
    hour: int = 7
    timezone: str = "Africa/Nairobi"
    notify_emails: Optional[List[str]] = None

class MemberAdd(BaseModel):
    email: EmailStr
    role: str = "member"

@router.post("/")
def create(ws: WorkspaceCreate, auth=Depends(require_verified_user)):
    owner = None
    if auth["type"] == "user":
        owner = auth["user"].email
    created = create_workspace(ws.name, ws.region, ws.primary_language, ws.owner_email or owner)
    log_action("workspace_created", f"Created workspace {created['name']}", workspace_id=created["id"],
               user_email=owner or "api")
    return created

@router.get("/")
def list_all(auth=Depends(get_current_user)):
    return list_workspaces()

@router.get("/{ws_id}")
def get_one(ws_id: str, auth=Depends(get_current_user)):
    ws = get_workspace(ws_id)
    if not ws:
        raise HTTPException(status_code=404, detail="Workspace not found")
    return ws

@router.patch("/{ws_id}")
def update(ws_id: str, body: WorkspaceUpdate, auth=Depends(require_verified_user)):
    if auth["type"] == "user":
        require_roles(ws_id, auth["user"].email, ["owner", "admin"])
    updated = update_workspace(ws_id, body.dict(exclude_unset=True))
    if not updated:
        raise HTTPException(status_code=404, detail="Workspace not found")
    log_action("workspace_updated", f"Updated workspace {ws_id}", workspace_id=ws_id,
               user_email=auth["user"].email if auth["type"] == "user" else "api")
    return updated

@router.post("/{ws_id}/schedule")
def configure_schedule(ws_id: str, config: ScheduleConfig, auth=Depends(require_verified_user)):
    """Only owner or admin can change the weekly brief schedule."""
    if auth["type"] == "user":
        require_roles(ws_id, auth["user"].email, ["owner", "admin"])

    updated = set_brief_schedule(
        ws_id,
        config.day_of_week,
        config.hour,
        config.timezone,
        config.notify_emails
    )
    if not updated:
        raise HTTPException(status_code=404, detail="Workspace not found")
    reload_schedules()
    log_action("schedule_configured", f"Schedule set for {ws_id}", workspace_id=ws_id,
               user_email=auth["user"].email if auth["type"] == "user" else "api")
    return {
        "message": "Weekly brief schedule configured and loaded into background worker",
        "workspace": updated
    }

@router.post("/{ws_id}/members")
def add_workspace_member(ws_id: str, body: MemberAdd, auth=Depends(require_verified_user)):
    """Only owner or admin can directly add members."""
    if auth["type"] == "user":
        require_roles(ws_id, auth["user"].email, ["owner", "admin"])

    member = add_member(ws_id, body.email, body.role)
    if not member:
        raise HTTPException(status_code=404, detail="Workspace not found")
    log_action("member_added", f"Added {body.email} as {body.role}", workspace_id=ws_id,
               user_email=auth["user"].email if auth["type"] == "user" else "api")
    return member
