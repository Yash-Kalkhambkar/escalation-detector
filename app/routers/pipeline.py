from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Ticket, EscalationLog, Lead, Followup, Deal
from app.schemas import PipelineTraceResponse

router = APIRouter()


@router.get("/trace/{email}", response_model=PipelineTraceResponse)
def trace_pipeline(email: str, db: Session = Depends(get_db)):
    """Trace complete customer journey across all pipeline stages"""
    
    # Query all pipeline stages
    tickets = db.query(Ticket).filter(Ticket.email == email).all()
    escalation_logs = db.query(EscalationLog).filter(EscalationLog.email == email).all()
    leads = db.query(Lead).filter(Lead.description.contains(email)).all()
    followups = db.query(Followup).filter(Followup.email == email).all()
    deals = db.query(Deal).filter(Deal.conversation.contains(email)).all()
    
    # Convert to dictionaries
    tickets_data = [
        {
            "id": t.id,
            "text": t.text,
            "category": t.category,
            "urgency": t.urgency,
            "status": t.status,
            "created_at": t.created_at.isoformat() if t.created_at else None
        }
        for t in tickets
    ]
    
    escalation_logs_data = [
        {
            "id": e.id,
            "ticket_id": e.ticket_id,
            "escalate": e.escalate,
            "reason": e.reason,
            "created_at": e.created_at.isoformat() if e.created_at else None
        }
        for e in escalation_logs
    ]
    
    leads_data = [
        {
            "id": l.id,
            "name": l.name,
            "company": l.company,
            "score": l.score,
            "created_at": l.created_at.isoformat() if l.created_at else None
        }
        for l in leads
    ]
    
    followups_data = [
        {
            "id": f.id,
            "prospect": f.prospect,
            "last_interaction": f.last_interaction,
            "days_since": f.days_since,
            "created_at": f.created_at.isoformat() if f.created_at else None
        }
        for f in followups
    ]
    
    deals_data = [
        {
            "id": d.id,
            "prospect": d.prospect,
            "stage": d.stage,
            "created_at": d.created_at.isoformat() if d.created_at else None
        }
        for d in deals
    ]
    
    # Calculate summary
    summary = {
        "total_stages": sum([
            1 if leads_data else 0,
            1 if followups_data else 0,
            1 if deals_data else 0,
            1 if tickets_data else 0,
            1 if escalation_logs_data else 0
        ]),
        "leads_count": len(leads_data),
        "followups_count": len(followups_data),
        "deals_count": len(deals_data),
        "tickets_count": len(tickets_data),
        "escalations_count": len(escalation_logs_data)
    }
    
    return PipelineTraceResponse(
        email=email,
        pipeline_stage="complete",
        tickets=tickets_data,
        escalation_logs=escalation_logs_data,
        leads=leads_data,
        followups=followups_data,
        deals=deals_data,
        summary=summary
    )
