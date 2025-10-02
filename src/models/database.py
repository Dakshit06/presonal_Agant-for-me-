"""
Database models for Agentice
"""

from sqlalchemy import Column, String, Integer, Float, DateTime, Boolean, JSON, ForeignKey, Text, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from enum import Enum
import uuid

Base = declarative_base()


def generate_uuid():
    return str(uuid.uuid4())


class User(Base):
    """User account"""
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    email = Column(String, unique=True, nullable=False, index=True)
    name = Column(String, nullable=False)
    timezone = Column(String, default="UTC")
    locale = Column(String, default="en-US")
    
    # Preferences
    preferences = Column(JSON, default=dict)
    consents = Column(JSON, default=dict)
    
    # Feature flags
    auto_apply_enabled = Column(Boolean, default=False)
    auto_profile_update_enabled = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    integrations = relationship("Integration", back_populates="user", cascade="all, delete-orphan")
    tasks = relationship("Task", back_populates="user", cascade="all, delete-orphan")
    events = relationship("Event", back_populates="user", cascade="all, delete-orphan")
    emails = relationship("Email", back_populates="user", cascade="all, delete-orphan")
    opportunities = relationship("Opportunity", back_populates="user", cascade="all, delete-orphan")
    resumes = relationship("Resume", back_populates="user", cascade="all, delete-orphan")
    applications = relationship("Application", back_populates="user", cascade="all, delete-orphan")
    changesets = relationship("Changeset", back_populates="user", cascade="all, delete-orphan")


class Integration(Base):
    """OAuth integration with external services"""
    __tablename__ = "integrations"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    provider = Column(String, nullable=False)  # google, microsoft, github, linkedin
    scopes = Column(JSON, default=list)
    access_token_encrypted = Column(Text)
    refresh_token_encrypted = Column(Text)
    expires_at = Column(DateTime)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship("User", back_populates="integrations")


class TaskStatus(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Task(Base):
    """Task management"""
    __tablename__ = "tasks"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    
    source = Column(String)  # email, calendar, manual
    title = Column(String, nullable=False)
    description = Column(Text)
    priority = Column(String)  # low, medium, high, urgent
    status = Column(SQLEnum(TaskStatus), default=TaskStatus.TODO)
    
    due_at = Column(DateTime)
    completed_at = Column(DateTime)
    
    created_from_email_id = Column(String, ForeignKey("emails.id"))
    labels = Column(JSON, default=list)
    confidence = Column(Float)  # AI confidence in task creation
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship("User", back_populates="tasks")


class Event(Base):
    """Calendar events"""
    __tablename__ = "events"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    
    calendar_id = Column(String)
    provider_event_id = Column(String)
    
    title = Column(String, nullable=False)
    description = Column(Text)
    location = Column(String)
    
    start_at = Column(DateTime, nullable=False)
    end_at = Column(DateTime, nullable=False)
    
    attendees = Column(JSON, default=list)
    prep_notes = Column(Text)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship("User", back_populates="events")


class Email(Base):
    """Email messages"""
    __tablename__ = "emails"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    
    provider_msg_id = Column(String, unique=True)
    thread_id = Column(String)
    
    from_email = Column(String)
    to_email = Column(String)
    subject = Column(String)
    snippet = Column(Text)
    body = Column(Text)
    
    received_at = Column(DateTime)
    triage_label = Column(String)  # action_required, fyi, archive, spam
    action_json = Column(JSON)  # AI-suggested actions
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="emails")
    tasks = relationship("Task", foreign_keys=[Task.created_from_email_id])


class OpportunityStatus(str, Enum):
    IDENTIFIED = "identified"
    REVIEWING = "reviewing"
    APPLYING = "applying"
    APPLIED = "applied"
    REJECTED = "rejected"
    EXPIRED = "expired"


class Opportunity(Base):
    """Job opportunities"""
    __tablename__ = "opportunities"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    
    source = Column(String)  # indeed, linkedin, glassdoor, manual
    title = Column(String, nullable=False)
    company = Column(String, nullable=False)
    location = Column(String)
    url = Column(String, nullable=False)
    
    description = Column(Text)
    requirements = Column(JSON)  # Extracted requirements
    salary_range = Column(JSON)
    
    tags = Column(JSON, default=list)
    fit_score = Column(Float)  # 0.0 to 1.0
    status = Column(SQLEnum(OpportunityStatus), default=OpportunityStatus.IDENTIFIED)
    
    discovered_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship("User", back_populates="opportunities")
    applications = relationship("Application", back_populates="opportunity")


class Resume(Base):
    """Resume versions"""
    __tablename__ = "resumes"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    
    title = Column(String, nullable=False)
    doc_url = Column(String)  # Path to file
    content_json = Column(JSON)  # Structured resume data
    
    is_current = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship("User", back_populates="resumes")


class ApplicationStatus(str, Enum):
    DRAFT = "draft"
    PENDING_APPROVAL = "pending_approval"
    APPROVED = "approved"
    REJECTED = "rejected"
    SUBMITTED = "submitted"
    UNDER_REVIEW = "under_review"
    INTERVIEWING = "interviewing"
    OFFERED = "offered"
    ACCEPTED = "accepted"
    DECLINED = "declined"
    FAILED = "failed"


class Application(Base):
    """Job applications"""
    __tablename__ = "applications"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    opportunity_id = Column(String, ForeignKey("opportunities.id"), nullable=False)
    
    resume_variant = Column(JSON)  # Customized resume
    cover_letter = Column(Text)
    
    status = Column(SQLEnum(ApplicationStatus), default=ApplicationStatus.DRAFT)
    confirmation_number = Column(String)
    
    submitted_at = Column(DateTime)
    response_at = Column(DateTime)
    
    notes = Column(Text)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship("User", back_populates="applications")
    opportunity = relationship("Opportunity", back_populates="applications")


class ChangesetStatus(str, Enum):
    DRAFT = "draft"
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    APPLIED = "applied"


class Changeset(Base):
    """Proposed changes requiring approval"""
    __tablename__ = "changesets"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    
    target = Column(String)  # resume, linkedin, github, portfolio
    target_id = Column(String)
    
    changes = Column(JSON)  # Structured diff
    rationale = Column(Text)
    
    status = Column(SQLEnum(ChangesetStatus), default=ChangesetStatus.DRAFT)
    
    reviewed_at = Column(DateTime)
    applied_at = Column(DateTime)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="changesets")


class ContentDraft(Base):
    """Generated content drafts"""
    __tablename__ = "content_drafts"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    
    type = Column(String)  # linkedin_post, article, case_study, etc.
    title = Column(String)
    body_md = Column(Text)
    
    seo_entities = Column(JSON, default=list)
    status = Column(String, default="draft")  # draft, published
    
    published_at = Column(DateTime)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship("User")


class Feedback(Base):
    """User feedback for ML improvement"""
    __tablename__ = "feedback"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    
    action = Column(String)  # Type of action
    result = Column(String)  # accepted, rejected, edited
    notes = Column(Text)
    
    feedback_metadata = Column(JSON, default=dict)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User")
