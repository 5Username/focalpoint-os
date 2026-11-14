"""
Workspace service with SQLite/Postgres persistence + analytics helpers.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import uuid
import secrets
from sqlalchemy.orm import Session
from app.db import WorkspaceModel, WorkspaceMemberModel, SessionLocal, init_db

init_db()

def _generate_api_key() -> str:
    return "fp_" + secrets.token_urlsafe(24)

def _to_dict(ws: WorkspaceModel, include_key: bool = True) -> Dict[str, Any]:
    data = {
        "id": ws.id,
        "name": ws.name,
        "region": ws.region,
        "primary_language": ws.primary_language,
        "created_at": ws.created_at.isoformat() + "Z" if ws.created_at else None,
        "analytics": {
            "briefs_generated": ws.briefs_generated or 0,
            "incidents_logged": ws.incidents_logged or 0,
            "last_brief_at": ws.last_brief_at.isoformat() + "Z" if ws.last_brief_at else None,
            "member_count": len(ws.members or [])
        },
        "settings": {
            "brief_schedule": {
                "enabled": ws.schedule_enabled,
                "day_of_week": ws.schedule_day,
                "hour": ws.schedule_hour,
                "timezone": ws.schedule_timezone
            } if ws.schedule_enabled else None,
            "notify_emails": [e.strip() for e in (ws.notify_emails or "").split(",") if e.strip()]
        },
        "members": [
            {"id": m.id, "email": m.email, "role": m.role}
            for m in (ws.members or [])
        ]
    }
    if include_key:
        data["api_key"] = ws.api_key
    return data

def create_workspace(name: str, region: str = "Kenya", primary_language: str = "en", owner_email: str = None) -> Dict[str, Any]:
    db: Session = SessionLocal()
    try:
        ws_id = str(uuid.uuid4())[:8]
        api_key = _generate_api_key()
        ws = WorkspaceModel(
            id=ws_id,
            name=name,
            region=region,
            primary_language=primary_language,
            api_key=api_key
        )
        db.add(ws)
        if owner_email:
            member = WorkspaceMemberModel(
                id=str(uuid.uuid4())[:8],
                workspace_id=ws_id,
                email=owner_email,
                role="owner"
            )
            db.add(member)
        db.commit()
        db.refresh(ws)
        return _to_dict(ws, include_key=True)
    finally:
        db.close()

def get_workspace(ws_id: str) -> Optional[Dict[str, Any]]:
    db = SessionLocal()
    try:
        ws = db.query(WorkspaceModel).filter(WorkspaceModel.id == ws_id).first()
        return _to_dict(ws) if ws else None
    finally:
        db.close()

def get_workspace_by_api_key(api_key: str) -> Optional[Dict[str, Any]]:
    db = SessionLocal()
    try:
        ws = db.query(WorkspaceModel).filter(WorkspaceModel.api_key == api_key).first()
        return _to_dict(ws) if ws else None
    finally:
        db.close()

def list_workspaces() -> List[Dict[str, Any]]:
    db = SessionLocal()
    try:
        rows = db.query(WorkspaceModel).all()
        return [_to_dict(ws, include_key=False) for ws in rows]
    finally:
        db.close()

def update_workspace(ws_id: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    db = SessionLocal()
    try:
        ws = db.query(WorkspaceModel).filter(WorkspaceModel.id == ws_id).first()
        if not ws:
            return None
        for k in ["name", "region", "primary_language"]:
            if k in updates and updates[k] is not None:
                setattr(ws, k, updates[k])
        if "notify_emails" in updates:
            emails = updates["notify_emails"]
            ws.notify_emails = ",".join(emails) if isinstance(emails, list) else str(emails)
        db.commit()
        db.refresh(ws)
        return _to_dict(ws)
    finally:
        db.close()

def set_brief_schedule(ws_id: str, day_of_week: str = "monday", hour: int = 7, timezone: str = "Africa/Nairobi", notify_emails: List[str] = None) -> Optional[Dict[str, Any]]:
    db = SessionLocal()
    try:
        ws = db.query(WorkspaceModel).filter(WorkspaceModel.id == ws_id).first()
        if not ws:
            return None
        ws.schedule_enabled = True
        ws.schedule_day = day_of_week.lower()
        ws.schedule_hour = hour
        ws.schedule_timezone = timezone
        if notify_emails is not None:
            ws.notify_emails = ",".join(notify_emails)
        db.commit()
        db.refresh(ws)
        return _to_dict(ws)
    finally:
        db.close()

def get_all_enabled_schedules() -> List[Dict[str, Any]]:
    db = SessionLocal()
    try:
        rows = db.query(WorkspaceModel).filter(WorkspaceModel.schedule_enabled == True).all()
        result = []
        for ws in rows:
            result.append({
                "workspace": _to_dict(ws),
                "schedule": {
                    "day_of_week": ws.schedule_day,
                    "hour": ws.schedule_hour,
                    "timezone": ws.schedule_timezone,
                    "enabled": True,
                    "notify_emails": [e.strip() for e in (ws.notify_emails or "").split(",") if e.strip()]
                }
            })
        return result
    finally:
        db.close()

def add_member(ws_id: str, email: str, role: str = "member") -> Optional[Dict[str, Any]]:
    if role not in ("owner", "admin", "member", "viewer"):
        role = "member"
    db = SessionLocal()
    try:
        ws = db.query(WorkspaceModel).filter(WorkspaceModel.id == ws_id).first()
        if not ws:
            return None
        member = WorkspaceMemberModel(
            id=str(uuid.uuid4())[:8],
            workspace_id=ws_id,
            email=email,
            role=role
        )
        db.add(member)
        db.commit()
        return {"id": member.id, "email": email, "role": role}
    finally:
        db.close()

def increment_brief_counter(ws_id: str):
    db = SessionLocal()
    try:
        ws = db.query(WorkspaceModel).filter(WorkspaceModel.id == ws_id).first()
        if ws:
            ws.briefs_generated = (ws.briefs_generated or 0) + 1
            ws.last_brief_at = datetime.utcnow()
            db.commit()
    finally:
        db.close()

def increment_incident_counter(ws_id: str):
    db = SessionLocal()
    try:
        ws = db.query(WorkspaceModel).filter(WorkspaceModel.id == ws_id).first()
        if ws:
            ws.incidents_logged = (ws.incidents_logged or 0) + 1
            db.commit()
    finally:
        db.close()

def get_workspace_analytics(ws_id: str) -> Optional[Dict[str, Any]]:
    ws = get_workspace(ws_id)
    if not ws:
        return None
    return {
        "workspace_id": ws_id,
        "name": ws["name"],
        "analytics": ws.get("analytics", {}),
        "schedule": ws.get("settings", {}).get("brief_schedule"),
        "member_count": len(ws.get("members", []))
    }
