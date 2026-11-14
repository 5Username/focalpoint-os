from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from app.services.workspaces import (
    create_workspace, get_workspace, list_workspaces,
    update_workspace, set_brief_schedule
)

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
    day_of_week: str = "monday"   # monday, tuesday, ...
    hour: int = 7                 # 0-23
    timezone: str = "Africa/Nairobi"

@router.post("/")
def create(ws: WorkspaceCreate):
    return create_workspace(ws.name, ws.region, ws.primary_language)

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
def update(ws_id: str, body: WorkspaceUpdate):
    ws = update_workspace(ws_id, body.dict(exclude_unset=True))
    if not ws:
        raise HTTPException(status_code=404, detail="Workspace not found")
    return ws

@router.post("/{ws_id}/schedule")
def configure_schedule(ws_id: str, config: ScheduleConfig):
    """Configure automated weekly brief generation for this NGO workspace."""
    ws = set_brief_schedule(ws_id, config.day_of_week, config.hour, config.timezone)
    if not ws:
        raise HTTPException(status_code=404, detail="Workspace not found")
    return {
        "message": "Weekly brief schedule configured",
        "workspace": ws,
        "note": "In production this would be picked up by a scheduler (APScheduler, Celery, or external cron / GitHub Actions)."
    }
