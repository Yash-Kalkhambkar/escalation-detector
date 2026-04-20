from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, text
from typing import List, Optional
from app.database import get_db
from app.models import EscalationLog, Ticket
from app.schemas import (
    ManualCheckRequest,
    FromTicketRequest,
    EscalationResponse,
    EscalationLogResponse,
    StatsResponse,
    HealthResponse
)
from app.services.llm import check_escalation

router = APIRouter()


@router.post("/check", response_model=EscalationResponse)
def manual_check(request: ManualCheckRequest, db: Session = Depends(get_db)):
    """Manual escalation check with custom input"""
    try:
        # Call LLM service
        result = check_escalation(request.conversation)
        
        # Create escalation log
        log = EscalationLog(
            ticket_id=request.ticket_id,
            conversation=request.conversation,
            escalate=result["escalate"],
            reason=result["reason"],
            email=request.email
        )
        db.add(log)
        db.commit()
        db.refresh(log)
        
        return EscalationResponse(
            ticket_id=request.ticket_id,
            email=request.email,
            escalate=result["escalate"],
            reason=result["reason"],
            log_id=log.id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/from-ticket", response_model=EscalationResponse)
def from_ticket_check(request: FromTicketRequest, db: Session = Depends(get_db)):
    """Pipeline-based escalation check from ticket ID"""
    # Query ticket
    ticket = db.query(Ticket).filter(Ticket.id == request.ticket_id).first()
    
    if not ticket:
        raise HTTPException(status_code=404, detail=f"Ticket {request.ticket_id} not found")
    
    # Construct enriched context
    context = f"""Category: {ticket.category}
Urgency: {ticket.urgency}
Status: {ticket.status}
Ticket Text: {ticket.text}
Draft Reply: {ticket.draft_reply or 'None'}"""
    
    try:
        # Call LLM service
        result = check_escalation(context)
        
        # Create escalation log
        log = EscalationLog(
            ticket_id=str(ticket.id),
            conversation=ticket.text,
            escalate=result["escalate"],
            reason=result["reason"],
            email=ticket.email or "unknown@example.com"
        )
        db.add(log)
        db.commit()
        db.refresh(log)
        
        return EscalationResponse(
            ticket_id=str(ticket.id),
            email=ticket.email or "unknown@example.com",
            escalate=result["escalate"],
            reason=result["reason"],
            log_id=log.id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/logs", response_model=List[EscalationLogResponse])
def get_logs(email: Optional[str] = None, db: Session = Depends(get_db)):
    """Retrieve escalation logs with optional email filter"""
    query = db.query(EscalationLog)
    
    if email:
        query = query.filter(EscalationLog.email == email)
    
    logs = query.order_by(EscalationLog.created_at.desc()).all()
    return logs


@router.get("/logs/ticket/{ticket_id}", response_model=List[EscalationLogResponse])
def get_ticket_logs(ticket_id: str, db: Session = Depends(get_db)):
    """Retrieve escalation logs for specific ticket"""
    logs = db.query(EscalationLog).filter(
        EscalationLog.ticket_id == ticket_id
    ).order_by(EscalationLog.created_at.desc()).all()
    return logs


@router.get("/stats", response_model=StatsResponse)
def get_stats(db: Session = Depends(get_db)):
    """Calculate escalation statistics"""
    total = db.query(func.count(EscalationLog.id)).scalar()
    escalated = db.query(func.count(EscalationLog.id)).filter(
        EscalationLog.escalate == True
    ).scalar()
    not_escalated = db.query(func.count(EscalationLog.id)).filter(
        EscalationLog.escalate == False
    ).scalar()
    
    escalation_rate = (escalated / total) if total > 0 else 0.0
    
    return StatsResponse(
        total=total,
        escalated=escalated,
        not_escalated=not_escalated,
        escalation_rate=escalation_rate
    )


@router.get("/health", response_model=HealthResponse)
def health_check(db: Session = Depends(get_db)):
    """Health check for database and LLM service"""
    # Test database
    try:
        db.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception:
        db_status = "disconnected"
    
    # Test LLM service
    try:
        check_escalation("Test prompt")
        llm_status = "operational"
    except Exception:
        llm_status = "unavailable"
    
    overall_status = "healthy" if db_status == "connected" and llm_status == "operational" else "degraded"
    
    return HealthResponse(
        status=overall_status,
        database=db_status,
        llm=llm_status
    )
