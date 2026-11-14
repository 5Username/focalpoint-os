from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import briefs, travel, incidents, pdf_export

app = FastAPI(
    title="FocalPoint OS",
    description="Toolkit for NGO Security Focal Points — Weekly Briefs, Travel Risk Packs, Offline Incident Reporting, PDF export, ethical OSINT",
    version="0.3.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(briefs.router, prefix="/api/briefs", tags=["Weekly Briefs"])
app.include_router(travel.router, prefix="/api/travel", tags=["Travel Risk Packs"])
app.include_router(incidents.router, prefix="/api/incidents", tags=["Incident Reports"])
app.include_router(pdf_export.router, prefix="/api/pdf", tags=["PDF Export"])

@app.get("/")
def root():
    return {
        "name": "FocalPoint OS",
        "status": "online",
        "version": "0.3.0",
        "modules": ["weekly-briefs", "travel-risk-packs", "offline-incidents", "pdf-export", "ethical-osint"]
    }
