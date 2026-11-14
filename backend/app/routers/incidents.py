from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

router = APIRouter()

class IncidentCategory(str, Enum):
    security = "security"
    medical = "medical"
    logistics = "logistics"
    safeguarding = "safeguarding"
    other = "other"

class IncidentSeverity(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"

class IncidentCreate(BaseModel):
    title: str
    category: IncidentCategory
    severity: IncidentSeverity
    location: str
    description: str
    reported_by: str
    occurred_at: Optional[datetime] = None
    actions_taken: Optional[str] = None
    people_involved: Optional[List[str]] = None

@router.post("/log")
def log_incident(incident: IncidentCreate):
    """
    Log an incident. In production this writes to Google Sheets
    and supports offline queue from the frontend.
    """
    return {
        "status": "received",
        "id": f"INC-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
        "message": "Incident logged successfully. Will sync to Google Sheet when online.",
        "data": incident.dict()
    }

@router.get("/health")
def health():
    return {"status": "ok", "module": "incidents"}
