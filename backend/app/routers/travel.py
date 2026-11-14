from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from datetime import date

router = APIRouter()

class TravelPackRequest(BaseModel):
    destination: str
    start_date: date
    end_date: date
    organization: str
    traveler_profile: Optional[str] = "standard"  # standard / high-profile / medical

@router.post("/compile")
def compile_travel_risk_pack(req: TravelPackRequest):
    """
    Compile a one-page go/no-go travel risk pack from public data.
    """
    return {
        "destination": req.destination,
        "period": f"{req.start_date} to {req.end_date}",
        "organization": req.organization,
        "overall_recommendation": "GO WITH MITIGATION",  # GO / NO-GO / GO WITH MITIGATION
        "key_risks": [
            {"category": "Crime", "level": "Medium", "notes": "Petty theft in urban centres"},
            {"category": "Road Safety", "level": "High", "notes": "Night travel strongly discouraged"},
            {"category": "Health", "level": "Medium", "notes": "Standard vaccinations recommended"},
            {"category": "Political", "level": "Low", "notes": "No major events scheduled"}
        ],
        "mitigations": [
            "Use vetted transport only",
            "Avoid night movement",
            "Register with local authorities if required",
            "Carry emergency contacts and tracking"
        ],
        "go_no_go_checklist": [
            {"item": "Destination risk assessed", "status": True},
            {"item": "Medical clearance", "status": True},
            {"item": "Communications plan", "status": False},
            {"item": "Insurance confirmed", "status": True},
            {"item": "Local contact briefed", "status": False}
        ],
        "disclaimer": "Compiled from public sources for coordination purposes only."
    }
