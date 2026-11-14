from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.routers import briefs, travel, incidents, pdf_export, workspaces, geo, auth, analytics, invites
from app.scheduler import start_scheduler, shutdown_scheduler, reload_schedules
from app.db import init_db
from app.middleware.rate_limit import RateLimitMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    start_scheduler()
    yield
    shutdown_scheduler()

app = FastAPI(
    title="FocalPoint OS",
    description="Advanced multi-tenant toolkit for NGO Security Focal Points",
    version="0.8.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rate limit auth endpoints (20 requests / minute / IP)
app.add_middleware(RateLimitMiddleware, max_requests=20, window_seconds=60)

app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(briefs.router, prefix="/api/briefs", tags=["Weekly Briefs"])
app.include_router(travel.router, prefix="/api/travel", tags=["Travel Risk Packs"])
app.include_router(incidents.router, prefix="/api/incidents", tags=["Incident Reports"])
app.include_router(pdf_export.router, prefix="/api/pdf", tags=["PDF Export"])
app.include_router(workspaces.router, prefix="/api/workspaces", tags=["NGO Workspaces"])
app.include_router(geo.router, prefix="/api/geo", tags=["GeoJSON & Mapping"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["Analytics"])
app.include_router(invites.router, prefix="/api/invites", tags=["Invites"])

@app.get("/")
def root():
    return {
        "name": "FocalPoint OS",
        "status": "online",
        "version": "0.8.0",
        "modules": [
            "user-login", "email-verification", "password-reset",
            "jwt-auth", "api-key-auth", "workspace-invites",
            "rate-limiting", "rbac", "audit-csv-export",
            "weekly-briefs", "travel-risk-packs", "offline-incidents",
            "pdf-export", "html-email", "ethical-osint",
            "multi-tenant-workspaces", "role-based-access",
            "crisis-mapping", "geojson-export",
            "brief-scheduling", "background-worker",
            "workspace-analytics", "audit-log",
            "sqlite-postgres"
        ]
    }

@app.get("/health")
def health():
    return {"status": "ok", "service": "focalpoint-os"}

@app.post("/api/admin/reload-schedules")
def admin_reload_schedules():
    reload_schedules()
    return {"status": "ok", "message": "Schedules reloaded"}
