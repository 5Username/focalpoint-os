"""
Simple audit log service.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
import uuid
from app.db import SessionLocal, AuditLogModel

def log_action(action: str, details: str = "", workspace_id: str = None, user_email: str = "system"):
    db = SessionLocal()
    try:
        entry = AuditLogModel(
            id=str(uuid.uuid4())[:8],
            workspace_id=workspace_id,
            user_email=user_email,
            action=action,
            details=details,
            created_at=datetime.utcnow()
        )
        db.add(entry)
        db.commit()
    finally:
        db.close()

def get_workspace_audit(workspace_id: str, limit: int = 50) -> List[Dict[str, Any]]:
    db = SessionLocal()
    try:
        rows = (
            db.query(AuditLogModel)
            .filter(AuditLogModel.workspace_id == workspace_id)
            .order_by(AuditLogModel.created_at.desc())
            .limit(limit)
            .all()
        )
        return [
            {
                "id": r.id,
                "action": r.action,
                "details": r.details,
                "user_email": r.user_email,
                "created_at": r.created_at.isoformat() + "Z" if r.created_at else None
            }
            for r in rows
        ]
    finally:
        db.close()

def get_recent_audit(limit: int = 30) -> List[Dict[str, Any]]:
    db = SessionLocal()
    try:
        rows = (
            db.query(AuditLogModel)
            .order_by(AuditLogModel.created_at.desc())
            .limit(limit)
            .all()
        )
        return [
            {
                "id": r.id,
                "workspace_id": r.workspace_id,
                "action": r.action,
                "details": r.details,
                "user_email": r.user_email,
                "created_at": r.created_at.isoformat() + "Z" if r.created_at else None
            }
            for r in rows
        ]
    finally:
        db.close()
