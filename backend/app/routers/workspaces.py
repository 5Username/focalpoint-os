from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from app.services.workspaces import (
    create_workspace, get_workspace, list_workspaces,
    update_workspace, set_brief_schedule, add_member
)
from app.auth import require_api_key
from app.scheduler import reload_schedules

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
    role: str = "member"  # owner | admin | member | viewer

@router.post("/")
def create(ws: WorkspaceCreate):
    created = create_workspace(ws.name, ws.region, ws.primary_language, ws.owner_email)
    return created

@router.get("/")
def list_all():
    return list_workspaces()

@router.get("/{ws_id}")
def get_one(ws_id: str):
    ws = get_workspace(ws_id)
    if not ws:
        raise HTTPException(status_code=404, detail="Workspace not found")
    return ws

@router.patch("/{ws_id}")
def update(ws_id: str, body: WorkspaceUpdate, ws=Depends(require_api_key)):
    if ws["id"] != ws_id:
        raise HTTPException(status_code=403, detail="API key does not match workspace")
    # Simple role check: only owner/admin can update
    # (In full system we would look up the calling user; here API key = workspace authority)
    updated = update_workspace(ws_id, body.dict(exclude_unset=True))
    if not updated:
        raise HTTPException(status_code=404, detail="Workspace not found")
    return updated

@router.post("/{ws_id}/schedule")
def configure_schedule(ws_id: str, config: ScheduleConfig, ws=Depends(require_api_key)):
    if ws["id"] != ws_id:
        raise HTTPException(status_code=403, detail="API key does not match workspace")
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
    return {
        "message": "Weekly brief schedule configured and loaded into background worker",
        "workspace": updated
    }

@router.post("/{ws_id}/members")
def add_workspace_member(ws_id: str, body: MemberAdd, ws=Depends(require_api_key)):
    if ws["id"] != ws_id:
        raise HTTPException(status_code=403, detail="API key does not match workspace")
    member = add_member(ws_id, body.email, body.role)
    if not member:
        raise HTTPException(status_code=404, detail="Workspace not found")
    return member
