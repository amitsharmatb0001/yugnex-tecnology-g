"""
FILE: models.py
PATH: yugnex/backend/database/models.py
PURPOSE: Defines the database schema (tables) using SQLAlchemy ORM.
WORKING:
    1. Imports types and Base class.
    2. Defines classes for Users, Projects, Conversations, Messages, etc.
    3. Configures relationships between tables.
USAGE:
    new_user = User(email="...", username="...")
    session.add(new_user)
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from sqlalchemy import String, Integer, Boolean, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from database.connection import Base

# --- Users Table ---
class User(Base):
    __tablename__ = "users"

    # Step 1: Primary Fields
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    username: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    role: Mapped[str] = mapped_column(String(50), default="user")
    preferences: Mapped[Dict[str, Any]] = mapped_column(JSON, default={})
    
    # Step 2: Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    # Step 3: Relationships
    projects: Mapped[List["Project"]] = relationship("Project", back_populates="user", cascade="all, delete-orphan")
    conversations: Mapped[List["Conversation"]] = relationship("Conversation", back_populates="user")


# --- Projects Table ---
class Project(Base):
    __tablename__ = "projects"

    # Step 1: Primary Fields
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    tech_stack: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="active")
    settings: Mapped[Dict[str, Any]] = mapped_column(JSON, default={})
    
    # Step 2: Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    # Step 3: Relationships
    user: Mapped["User"] = relationship("User", back_populates="projects")
    conversations: Mapped[List["Conversation"]] = relationship("Conversation", back_populates="project", cascade="all, delete-orphan")
    memory: Mapped[List["ProjectMemory"]] = relationship("ProjectMemory", back_populates="project", cascade="all, delete-orphan")


# --- Conversations Table ---
class Conversation(Base):
    __tablename__ = "conversations"

    # Step 1: Primary Fields
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    project_id: Mapped[Optional[int]] = mapped_column(ForeignKey("projects.id"), nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    title: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    mode: Mapped[str] = mapped_column(String(50), default="chat")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    # Step 2: Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    # Step 3: Relationships
    user: Mapped["User"] = relationship("User", back_populates="conversations")
    project: Mapped[Optional["Project"]] = relationship("Project", back_populates="conversations")
    messages: Mapped[List["Message"]] = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")
    agent_logs: Mapped[List["AgentLog"]] = relationship("AgentLog", back_populates="conversation", cascade="all, delete-orphan")


# --- Messages Table ---
class Message(Base):
    __tablename__ = "messages"

    # Step 1: Primary Fields
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    conversation_id: Mapped[int] = mapped_column(ForeignKey("conversations.id"), nullable=False)
    role: Mapped[str] = mapped_column(String(20), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    agent_key: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    model_used: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    tokens_used: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    metadata_json: Mapped[Dict[str, Any]] = mapped_column("metadata", JSON, default={})
    
    # Step 2: Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    # Step 3: Relationships
    conversation: Mapped["Conversation"] = relationship("Conversation", back_populates="messages")


# --- Project Memory Table ---
class ProjectMemory(Base):
    __tablename__ = "project_memory"

    # Step 1: Primary Fields
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), nullable=False)
    memory_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    importance: Mapped[int] = mapped_column(Integer, default=5)
    
    # Step 2: Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    # Step 3: Relationships
    project: Mapped["Project"] = relationship("Project", back_populates="memory")


# --- Agent Logs Table ---
class AgentLog(Base):
    __tablename__ = "agent_logs"

    # Step 1: Primary Fields
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    conversation_id: Mapped[int] = mapped_column(ForeignKey("conversations.id"), nullable=False)
    agent_key: Mapped[str] = mapped_column(String(50), nullable=False)
    action: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    input_summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    output_summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    duration_ms: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    
    # Step 2: Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    # Step 3: Relationships
    conversation: Mapped["Conversation"] = relationship("Conversation", back_populates="agent_logs")