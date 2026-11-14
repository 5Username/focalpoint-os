"""
Simple multi-tenant NGO workspace support.
In-memory for demo purposes. Replace with database in production.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import uuid

# In-memory store (replace with Postgres/SQLite later)
_workspaces: Dict[str, Dict[str, Any]] = {}

def create_workspace(name: str, region: str = "Kenya", primary_language: str = "en") -> Dict[str, Any]:
    ws_id = str(uuid.uuid4())[:8]
    workspace = {
        "id": ws_id,
        "name": name,
        "region": region,
        "primary_language": primary_language,
        "created_at": datetime.utcnow().isoformat() + "Z",
        "settings": {
            "default_focus_areas": ["crime", "political", "health", "humanitarian"],
            "brief_schedule": None  # will hold cron-like config
        }
    }
    _workspaces[ws_id] = workspace
    return workspace

def get_workspace(ws_id: str) -> Optional[Dict[str, Any]]:
    return _workspaces.get(ws_id)

def list_workspaces() -> List[Dict[str, Any]]:
    return list(_workspaces.values())

def update_workspace(ws_id: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    ws = _workspaces.get(ws_id)
    if not ws:
        return None
    ws.update({k: v for k, v in updates.items() if k in ["name", "region", "primary_language"]})
    if "settings" in updates:
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
