"""
SQLite persistence (swap to Postgres by changing DATABASE_URL).
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

class WorkspaceModel(Base):
    __tablename__ = "workspaces"

    id = Column(String(16), primary_key=True)
    name = Column(String(255), nullable=False)
    region = Column(String(100), default="Kenya")
    primary_language = Column(String(10), default="en")
    api_key = Column(String(64), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Schedule
    schedule_enabled = Column(Boolean, default=False)
    schedule_day = Column(String(20), default="monday")
    schedule_hour = Column(Integer, default=7)
    schedule_timezone = Column(String(50), default="Africa/Nairobi")

    # Email delivery
    notify_emails = Column(Text, default="")  # comma-separated

    members = relationship("WorkspaceMemberModel", back_populates="workspace", cascade="all, delete-orphan")

class WorkspaceMemberModel(Base):
    __tablename__ = "workspace_members"

    id = Column(String(16), primary_key=True)
    workspace_id = Column(String(16), ForeignKey("workspaces.id"), nullable=False)
    email = Column(String(255), nullable=False)
    role = Column(String(20), default="member")  # owner | admin | member | viewer
    created_at = Column(DateTime, default=datetime.utcnow)

    workspace = relationship("WorkspaceModel", back_populates="members")

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
