from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional
from datetime import date

router = APIRouter()

class BriefRequest(BaseModel):
    organization: str
    region: str = "Kenya"
    focus_areas: Optional[List[str]] = ["crime", "political", "terrorism", "health"]
    week_of: Optional[date] = None

@router.post("/generate")
def generate_weekly_brief(req: BriefRequest):
    """
    Generate a structured weekly security brief.
    In production this pulls public OSINT sources.
    Currently returns a high-quality template structure.
    """
    return {
        "title": f"Weekly Security Brief — {req.organization}",
        "region": req.region,
        "week_of": str(req.week_of or date.today()),
        "sections": {
            "executive_summary": "Placeholder: Key developments this week.",
            "crime_and_banditry": "Public source summary would appear here.",
            "political_security": "Public source summary would appear here.",
            "terrorism_and_extremism": "Public source summary would appear here.",
            "health_and_disease": "Public source summary would appear here.",
            "recommendations": [
                "Maintain current posture",
                "Review travel to high-risk counties",
                "Update staff briefing cascade"
            ]
        },
        "disclaimer": "This is a research and coordination product compiled from public sources. It is not licensed security advice."
    }
