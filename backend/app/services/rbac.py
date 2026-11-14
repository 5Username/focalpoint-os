"""
Role-based access helpers.
"""

from typing import Optional, List
from fastapi import HTTPException
from app.db import SessionLocal, WorkspaceMemberModel

def get_member_role(workspace_id: str, email: str) -> Optional[str]:
    db = SessionLocal()
    try:
        member = (
            db.query(WorkspaceMemberModel)
            .filter(
                WorkspaceMemberModel.workspace_id == workspace_id,
                WorkspaceMemberModel.email == email.lower()
            )
            .first()
        )
        return member.role if member else None
    finally:
        db.close()

def require_roles(workspace_id: str, email: str, allowed: List[str]):
    """Raise 403 if the user does not have one of the allowed roles in the workspace."""
    role = get_member_role(workspace_id, email)
    if role is None or role not in allowed:
        raise HTTPException(
            status_code=403,
            detail=f"Requires one of these roles: {', '.join(allowed)}. Your role: {role or 'none'}"
        )
    return role
