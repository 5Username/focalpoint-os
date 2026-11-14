"""
Multi-tenant NGO workspace support with simple API keys.
In-memory store for demo. Replace with database in production.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import uuid
import secrets

_workspaces: Dict[str, Dict[str, Any]] = {}

def _generate_api_key() -> str:
    return "fp_" + secrets.token_urlsafe(24)

def create_workspace(name: str, region: str = "Kenya", primary_language: str = "en") -> Dict[str, Any]:
    ws_id = str(uuid.uuid4())[:8]
    api_key = _generate_api_key()
    workspace = {
        "id": ws_id,
        "name": name,
        "region": region,
        "primary_language": primary_language,
        "api_key": api_key,
        "created_at": datetime.utcnow().isoformat() + "Z",
        "settings": {
            "default_focus_areas": ["crime", "political", "health", "humanitarian"],
            "brief_schedule": None
        }
    }
    _workspaces[ws_id] = workspace
    return workspace

def get_workspace(ws_id: str) -> Optional[Dict[str, Any]]:
    return _workspaces.get(ws_id)

def get_workspace_by_api_key(api_key: str) -> Optional[Dict[str, Any]]:
    for ws in _workspaces.values():
        if ws.get("api_key") == api_key:
            return ws
    return None

def list_workspaces() -> List[Dict[str, Any]]:
    # Return without exposing full api_key in list views if desired
    return list(_workspaces.values())

def update_workspace(ws_id: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    ws = _workspaces.get(ws_id)
    if not ws:
        return None
    for k in ["name", "region", "primary_language"]:
        if k in updates and updates[k] is not None:
            ws[k] = updates[k]
    if "settings" in updates and updates["settings"]:
        ws["settings"].update(updates["settings"])
    return ws

def set_brief_schedule(ws_id: str, day_of_week: str = "monday", hour: int = 7, timezone: str = "Africa/Nairobi") -> Optional[Dict[str, Any]]:
    ws = _workspaces.get(ws_id)
    if not ws:
        return None
    ws["settings"]["brief_schedule"] = {
        "day_of_week": day_of_week.lower(),
        "hour": hour,
        "timezone": timezone,
        "enabled": True,
        "updated_at": datetime.utcnow().isoformat() + "Z"
    }
    return ws

def get_all_enabled_schedules() -> List[Dict[str, Any]]:
    result = []
    for ws in _workspaces.values():
        sched = ws.get("settings", {}).get("brief_schedule")
        if sched and sched.get("enabled"):
            result.append({"workspace": ws, "schedule": sched})
    return result
