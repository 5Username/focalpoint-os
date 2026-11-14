from fastapi import APIRouter, HTTPException, Depends, Response
from app.services.workspaces import get_workspace_analytics, list_workspaces
from app.services.audit import get_workspace_audit, get_recent_audit
from app.auth import get_current_user
import csv
import io

router = APIRouter()

@router.get("/workspaces/{ws_id}")
def workspace_analytics(ws_id: str, auth=Depends(get_current_user)):
    data = get_workspace_analytics(ws_id)
    if not data:
        raise HTTPException(status_code=404, detail="Workspace not found")
    data["recent_activity"] = get_workspace_audit(ws_id, limit=20)
    return data

@router.get("/summary")
def analytics_summary(auth=Depends(get_current_user)):
    workspaces = list_workspaces()
    total_briefs = sum(w.get("analytics", {}).get("briefs_generated", 0) for w in workspaces)
    total_incidents = sum(w.get("analytics", {}).get("incidents_logged", 0) for w in workspaces)
    return {
        "workspace_count": len(workspaces),
        "total_briefs_generated": total_briefs,
        "total_incidents_logged": total_incidents,
        "workspaces": [
            {
                "id": w["id"],
                "name": w["name"],
                "briefs": w.get("analytics", {}).get("briefs_generated", 0),
                "incidents": w.get("analytics", {}).get("incidents_logged", 0),
                "last_brief_at": w.get("analytics", {}).get("last_brief_at")
            }
            for w in workspaces
        ],
        "recent_activity": get_recent_audit(limit=15)
    }

@router.get("/workspaces/{ws_id}/audit.csv")
def export_audit_csv(ws_id: str, auth=Depends(get_current_user)):
    """Export workspace audit log as CSV."""
    rows = get_workspace_audit(ws_id, limit=500)
    if not rows and not get_workspace_analytics(ws_id):
        raise HTTPException(status_code=404, detail="Workspace not found")

    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=["id", "action", "details", "user_email", "created_at"])
    writer.writeheader()
    for r in rows:
        writer.writerow(r)

    return Response(
        content=output.getvalue(),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=audit-{ws_id}.csv"}
    )
