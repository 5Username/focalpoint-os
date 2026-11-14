from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional
from datetime import date
from app.services.osint import build_brief_sections

router = APIRouter()

class BriefRequest(BaseModel):
    organization: str
    region: str = "Kenya"
    focus_areas: Optional[List[str]] = ["crime", "political", "terrorism", "health"]
    week_of: Optional[date] = None
    language: str = "en"  # en, sw, fr, ar

@router.post("/generate")
def generate_weekly_brief(req: BriefRequest):
    sections = build_brief_sections(req.region)

    return {
        "title": f"Weekly Security Brief — {req.organization}",
        "region": req.region,
        "week_of": str(req.week_of or date.today()),
        "language": req.language,
        "sections": sections,
        "disclaimer": "This is a research and coordination product compiled from public sources. It is not licensed security advice.",
        "generated_at": date.today().isoformat()
    }
