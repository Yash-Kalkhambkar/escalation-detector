from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class ManualCheckRequest(BaseModel):
    ticket_id: str
    conversation: str
    email: str


class FromTicketRequest(BaseModel):
    ticket_id: int


class EscalationResponse(BaseModel):
    ticket_id: str
    email: str
    escalate: bool
    reason: str
    log_id: int


class EscalationLogResponse(BaseModel):
    id: int
    ticket_id: str
    conversation: str
    escalate: bool
    reason: str
    email: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True


class StatsResponse(BaseModel):
    total: int
    escalated: int
    not_escalated: int
    escalation_rate: float


class HealthResponse(BaseModel):
    status: str
    database: str
    llm: str


class PipelineTraceResponse(BaseModel):
    email: str
    pipeline_stage: str
    tickets: List[dict]
    escalation_logs: List[dict]
    leads: List[dict]
    followups: List[dict]
    deals: List[dict]
    summary: dict
