from fastapi import APIRouter, Response
from pydantic import BaseModel
from typing import Any, Dict
from app.services.pdf import generate_brief_pdf, generate_travel_pdf

router = APIRouter()

class PDFRequest(BaseModel):
    type: str  # "brief" or "travel"
    data: Dict[str, Any]

@router.post("/generate")
def create_pdf(req: PDFRequest):
    if req.type == "brief":
        pdf_bytes = generate_brief_pdf(req.data)
        filename = "weekly-security-brief.pdf"
    elif req.type == "travel":
        pdf_bytes = generate_travel_pdf(req.data)
        filename = "travel-risk-pack.pdf"
    else:
        return {"error": "type must be 'brief' or 'travel'"}

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
