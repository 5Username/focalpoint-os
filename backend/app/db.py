"""
Database layer — SQLite by default, Postgres when DATABASE_URL is set.
Includes users, workspaces, members, audit log, and invites.
"""

from sqlalchemy import create_engine, Column, String, DateTime, Boolean, Integer, Text, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from datetime import datetime
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./focalpoint.db")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class UserModel(Base):
    __tablename__ = "users"

    id = Column(String(16), primary_key=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    full_name = Column(String(255), default="")
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    verification_token = Column(String(64), nullable=True)
    reset_token = Column(String(64), nullable=True)
    reset_token_expires = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    memberships = relationship("WorkspaceMemberModel", back_populates="user")

class WorkspaceModel(Base):
    __tablename__ = "workspaces"

    id = Column(String(16), primary_key=True)
    name = Column(String(255), nullable=False)
    region = Column(String(100), default="Kenya")
    primary_language = Column(String(10), default="en")
    api_key = Column(String(64), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    schedule_enabled = Column(Boolean, default=False)
    schedule_day = Column(String(20), default="monday")
    schedule_hour = Column(Integer, default=7)
    schedule_timezone = Column(String(50), default="Africa/Nairobi")
    notify_emails = Column(Text, default="")

    briefs_generated = Column(Integer, default=0)
    incidents_logged = Column(Integer, default=0)
    last_brief_at = Column(DateTime, nullable=True)

    members = relationship("WorkspaceMemberModel", back_populates="workspace", cascade="all, delete-orphan")
    audit_logs = relationship("AuditLogModel", back_populates="workspace", cascade="all, delete-orphan")
    invites = relationship("InviteModel", back_populates="workspace", cascade="all, delete-orphan")

class WorkspaceMemberModel(Base):
    __tablename__ = "workspace_members"

    id = Column(String(16), primary_key=True)
    workspace_id = Column(String(16), ForeignKey("workspaces.id"), nullable=False)
    user_id = Column(String(16), ForeignKey("users.id"), nullable=True)
    email = Column(String(255), nullable=False)
    role = Column(String(20), default="member")
    created_at = Column(DateTime, default=datetime.utcnow)

    workspace = relationship("WorkspaceModel", back_populates="members")
    user = relationship("UserModel", back_populates="memberships")

class AuditLogModel(Base):
    __tablename__ = "audit_logs"

    id = Column(String(16), primary_key=True)
    workspace_id = Column(String(16), ForeignKey("workspaces.id"), nullable=True)
    user_email = Column(String(255), default="system")
    action = Column(String(100), nullable=False)
    details = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)

    workspace = relationship("WorkspaceModel", back_populates="audit_logs")

class InviteModel(Base):
    __tablename__ = "invites"

    id = Column(String(16), primary_key=True)
    workspace_id = Column(String(16), ForeignKey("workspaces.id"), nullable=False)
    email = Column(String(255), nullable=False)
    role = Column(String(20), default="member")
    token = Column(String(64), unique=True, nullable=False)
    invited_by = Column(String(255), default="")
    accepted = Column(Boolean, default=False)
    expires_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    workspace = relationship("WorkspaceModel", back_populates="invites")

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
