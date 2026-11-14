from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import briefs, travel, incidents

app = FastAPI(
    title="FocalPoint OS",
    description="Toolkit for NGO Security Focal Points — Weekly Briefs, Travel Risk Packs, Offline Incident Reporting",
    version="0.1.0"
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

@app.get("/")
def root():
    return {
        "name": "FocalPoint OS",
        "status": "online",
        "modules": ["weekly-briefs", "travel-risk-packs", "offline-incidents"]
    }
