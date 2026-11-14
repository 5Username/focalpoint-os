from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from app.services.workspaces import (
    create_workspace, get_workspace, list_workspaces,
    update_workspace, set_brief_schedule
)
from app.auth import require_api_key
from app.scheduler import reload_schedules

router = APIRouter()

class WorkspaceCreate(BaseModel):
    name: str
    region: str = "Kenya"
    primary_language: str = "en"

class WorkspaceUpdate(BaseModel):
    name: Optional[str] = None
    region: Optional[str] = None
    primary_language: Optional[str] = None

class ScheduleConfig(BaseModel):
    day_of_week: str = "monday"
    hour: int = 7
    timezone: str = "Africa/Nairobi"

@router.post("/")
def create(ws: WorkspaceCreate):
    """Create a new NGO workspace. Returns the workspace including the API key (shown only once)."""
    created = create_workspace(ws.name, ws.region, ws.primary_language)
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
    updated = update_workspace(ws_id, body.dict(exclude_unset=True))
    if not updated:
        raise HTTPException(status_code=404, detail="Workspace not found")
    return updated

@router.post("/{ws_id}/schedule")
def configure_schedule(ws_id: str, config: ScheduleConfig, ws=Depends(require_api_key)):
    if ws["id"] != ws_id:
        raise HTTPException(status_code=403, detail="API key does not match workspace")
    updated = set_brief_schedule(ws_id, config.day_of_week, config.hour, config.timezone)
    if not updated:
        raise HTTPException(status_code=404, detail="Workspace not found")
    reload_schedules()  # immediately refresh the background worker
    return {
        "message": "Weekly brief schedule configured and loaded into background worker",
        "workspace": updated
    }
