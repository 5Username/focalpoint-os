from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.routers import briefs, travel, incidents, pdf_export, workspaces, geo
from app.scheduler import start_scheduler, shutdown_scheduler, reload_schedules

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    start_scheduler()
    yield
    # Shutdown
    shutdown_scheduler()

app = FastAPI(
    title="FocalPoint OS",
    description="Advanced multi-tenant toolkit for NGO Security Focal Points",
    version="0.5.0",
    lifespan=lifespan
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
app.include_router(workspaces.router, prefix="/api/workspaces", tags=["NGO Workspaces"])
app.include_router(geo.router, prefix="/api/geo", tags=["GeoJSON & Mapping"])

@app.get("/")
def root():
    return {
        "name": "FocalPoint OS",
        "status": "online",
        "version": "0.5.0",
        "modules": [
            "weekly-briefs", "travel-risk-packs", "offline-incidents",
            "pdf-export", "ethical-osint", "multi-tenant-workspaces",
            "api-key-auth", "crisis-mapping", "geojson-export",
            "brief-scheduling", "background-worker"
        ]
    }

@app.post("/api/admin/reload-schedules")
def admin_reload_schedules():
    """Manually reload all workspace schedules into the background worker."""
    reload_schedules()
    return {"status": "ok", "message": "Schedules reloaded"}
