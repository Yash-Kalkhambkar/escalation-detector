from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from sqlalchemy.sql import func
from app.database import Base


class EscalationLog(Base):
    __tablename__ = "escalation_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(String, nullable=False)
    conversation = Column(Text, nullable=False)
    escalate = Column(Boolean, nullable=False)
    reason = Column(String, nullable=False)
    email = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Ticket(Base):
    __tablename__ = "tickets"
    
    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    email = Column(String, nullable=False)
    category = Column(String, nullable=False)
    urgency = Column(String, nullable=False)
    status = Column(String, nullable=False)
    draft_reply = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Lead(Base):
    __tablename__ = "leads"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    company = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    score = Column(Integer, nullable=False)
    score_reason = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Followup(Base):
    __tablename__ = "followups"
    
    id = Column(Integer, primary_key=True, index=True)
    prospect = Column(String, nullable=False)
    last_interaction = Column(String, nullable=False)
    days_since = Column(Integer, nullable=False)
    email = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Deal(Base):
    __tablename__ = "deals"
    
    id = Column(Integer, primary_key=True, index=True)
    prospect = Column(String, nullable=False)
    conversation = Column(Text, nullable=False)
    stage = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
