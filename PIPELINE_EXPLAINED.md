# Understanding the B2B CRM Pipeline

## What is a Pipeline?

A **pipeline** is a series of connected stages that data flows through, where each stage performs a specific task and passes the results to the next stage. Think of it like an assembly line in a factory - each station does one job, and the product moves from station to station until it's complete.

In our case, this is a **B2B CRM (Customer Relationship Management) pipeline** that tracks a customer's journey from initial contact to support ticket escalation.

## The 5-Stage Pipeline Overview

```
Stage 1: LEADS → Stage 2: FOLLOWUPS → Stage 3: DEALS → Stage 4: TICKETS → Stage 5: ESCALATION
```

### 🔗 The Pipeline Connector: Email

**Every stage is connected by the customer's email address.** This is the "thread" that ties all stages together, allowing us to trace a customer's complete journey through the system.

---

## Stage 1: Lead Scoring

**What it does:** Captures initial information about potential customers (leads) and scores them based on their potential value.

**Database Table:** `leads`

**Key Fields:**
- `name` - Lead's name
- `company` - Company name
- `description` - Details about the lead
- `score` - Numerical score (0-100)
- `score_reason` - Why this score was given
- `created_at` - When the lead was captured

**Example:**
```json
{
  "name": "John Smith",
  "company": "TechCorp Inc",
  "description": "Interested in enterprise plan",
  "score": 85,
  "score_reason": "High budget, urgent need"
}
```

**Note:** Stage 1 doesn't have an email field in the database schema. Email information is embedded in the description field.

---

## Stage 2: Follow-up Tracking

**What it does:** Tracks follow-up activities with prospects and monitors how long it's been since the last interaction.

**Database Table:** `followups`

**Key Fields:**
- `prospect` - Name of the prospect
- `last_interaction` - Description of last contact
- `days_since` - Days since last interaction
- `email` - Customer email (pipeline identifier)
- `created_at` - When the follow-up was logged

**Example:**
```json
{
  "prospect": "John Smith",
  "last_interaction": "Demo call scheduled",
  "days_since": 3,
  "email": "john@techcorp.com"
}
```

**Pipeline Connection:** The `email` field connects this stage to other stages.

---

## Stage 3: Deal Management

**What it does:** Manages sales conversations and tracks deal progression through different stages (e.g., negotiation, proposal, closing).

**Database Table:** `deals`

**Key Fields:**
- `prospect` - Name of the prospect
- `conversation` - Sales conversation history
- `stage` - Current deal stage (e.g., "negotiation", "proposal")
- `created_at` - When the deal was created

**Example:**
```json
{
  "prospect": "John Smith",
  "conversation": "Discussed pricing for 50 user licenses",
  "stage": "negotiation"
}
```

**Note:** Stage 3 doesn't have a direct email field. Email is embedded in the conversation text.

---

## Stage 4: Ticket Classification

**What it does:** Receives customer support tickets, classifies them by category and urgency, and generates draft responses.

**Database Table:** `tickets`

**Key Fields:**
- `text` - The support ticket content
- `email` - Customer email (pipeline identifier)
- `category` - Ticket category (e.g., "billing", "technical")
- `urgency` - Urgency level (e.g., "high", "medium", "low")
- `status` - Ticket status (e.g., "open", "in_progress")
- `draft_reply` - AI-generated draft response
- `created_at` - When the ticket was created

**Example:**
```json
{
  "text": "I can't access my account after the update",
  "email": "john@techcorp.com",
  "category": "technical",
  "urgency": "high",
  "status": "open",
  "draft_reply": "We apologize for the inconvenience..."
}
```

**Pipeline Connection:** This is where **Stage 5 (our application)** reads from.

---

## Stage 5: Escalation Detection (Our Application)

**What it does:** Analyzes support tickets using AI to determine if they need immediate escalation to a human agent.

**Database Table:** `escalation_logs`

**Key Fields:**
- `ticket_id` - Reference to the ticket (as string)
- `conversation` - The ticket text that was analyzed
- `escalate` - Boolean decision (true = escalate, false = don't escalate)
- `reason` - Explanation for the decision
- `email` - Customer email (pipeline identifier)
- `created_at` - When the analysis was performed

**Example:**
```json
{
  "ticket_id": "123",
  "conversation": "I can't access my account...",
  "escalate": true,
  "reason": "High urgency technical issue affecting business operations",
  "email": "john@techcorp.com"
}
```

**How it works:**
1. Reads a ticket from Stage 4 (`tickets` table)
2. Sends ticket details to Groq AI (LLM)
3. AI analyzes and decides: escalate or not?
4. Stores the decision in `escalation_logs` table
5. Returns the decision to the user

---

## How the Pipeline Flows

### Example Customer Journey

Let's follow "john@techcorp.com" through the entire pipeline:

**Stage 1 - Lead Captured:**
```
John Smith from TechCorp shows interest
Score: 85/100 (high potential)
```

**Stage 2 - Follow-up:**
```
3 days since demo call
Status: Waiting for decision
```

**Stage 3 - Deal Created:**
```
Negotiating 50-user enterprise license
Stage: Proposal sent
```

**Stage 4 - Support Ticket:**
```
John reports: "Can't access account after update"
Category: Technical
Urgency: High
```

**Stage 5 - Escalation Check (Our App):**
```
AI Analysis: ESCALATE = TRUE
Reason: "High-value customer with urgent technical issue"
Action: Route to senior support agent immediately
```

### Tracing the Journey

Our application provides a **Pipeline Trace** endpoint that shows this complete journey:

```bash
GET /pipeline/trace/john@techcorp.com
```

**Response:**
```json
{
  "email": "john@techcorp.com",
  "pipeline_stage": "Stage 5 — Escalation Detector",
  "leads": [...],
  "followups": [...],
  "deals": [...],
  "tickets": [...],
  "escalation_logs": [...],
  "summary": {
    "total_stages": 5,
    "total_tickets": 1,
    "total_escalations": 1,
    "was_escalated": true
  }
}
```

---

## Why This Pipeline Architecture?

### Benefits:

1. **Separation of Concerns:** Each stage does one thing well
2. **Scalability:** Each stage can be scaled independently
3. **Maintainability:** Easy to update one stage without affecting others
4. **Traceability:** Complete customer journey tracking via email
5. **Modularity:** Stages can be developed by different teams

### Real-World Use Case:

Imagine a SaaS company with 10,000 customers:
- **Stage 1-2:** Marketing team manages leads and follow-ups
- **Stage 3:** Sales team manages deals
- **Stage 4:** Support team handles tickets
- **Stage 5:** AI automatically escalates critical issues to senior agents

Without this pipeline, all this data would be in one giant system, making it hard to manage and scale.

---

## What's New in Version 2 (Pipeline Edition)?

### Version 1 (Standalone)
- ❌ No connection to other systems
- ❌ Manual ticket input only
- ❌ No customer journey tracking
- ❌ Limited context for decisions

### Version 2 (Pipeline Edition)
- ✅ **Integrated with Stage 4:** Automatically reads from `tickets` table
- ✅ **Pipeline Trace:** View complete customer journey across all 5 stages
- ✅ **Enriched Context:** Uses ticket category, urgency, status, and draft reply for better AI decisions
- ✅ **Email-Based Filtering:** Filter logs and traces by customer email
- ✅ **Read-Only Access:** Safely reads from all pipeline stages without modifying them
- ✅ **Better Decision Making:** AI has more context (ticket metadata) for escalation decisions

### Key Improvements:

#### 1. **From-Ticket Endpoint** (New in V2)
```python
POST /escalation/from-ticket
Body: {"ticket_id": 123}
```
- Automatically fetches ticket from Stage 4
- Enriches context with category, urgency, status
- No need to manually copy ticket text

#### 2. **Pipeline Trace Endpoint** (New in V2)
```python
GET /pipeline/trace/customer@example.com
```
- Shows customer's complete journey
- Aggregates data from all 5 stages
- Helps understand escalation context

#### 3. **Email-Based Filtering** (New in V2)
```python
GET /escalation/logs?email=customer@example.com
```
- Filter logs by customer email
- Track escalation history per customer

#### 4. **Enriched AI Context** (New in V2)

**Version 1:**
```
"Analyze this ticket: I can't login"
```

**Version 2:**
```
"Analyze this ticket:
Category: Technical
Urgency: High
Status: Open
Draft Reply: We apologize for the inconvenience...
Ticket Text: I can't login"
```

The AI now has much more context to make better escalation decisions!

---

## Technical Implementation

### Database Design

**Read-Only Tables** (we never modify these):
- `leads` (Stage 1)
- `followups` (Stage 2)
- `deals` (Stage 3)
- `tickets` (Stage 4)

**Read-Write Table** (we create records here):
- `escalation_logs` (Stage 5 - our output)

### Pipeline Safety

Our application follows these rules:
1. **Never modify** tickets or other pipeline stage data
2. **Only read** from upstream stages (1-4)
3. **Only write** to our own table (escalation_logs)
4. **Always include email** for pipeline traceability

### Code Example: Pipeline Integration

```python
# Read from Stage 4 (tickets table)
ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()

# Enrich context with pipeline data
context = f"""
Ticket Category: {ticket.category}
Urgency: {ticket.urgency}
Status: {ticket.status}
Draft Reply: {ticket.draft_reply}
Ticket Text: {ticket.text}
"""

# Call AI for analysis
result = check_escalation(context)

# Write to Stage 5 (escalation_logs table)
log = EscalationLog(
    ticket_id=str(ticket.id),
    conversation=ticket.text,
    escalate=result["escalate"],
    reason=result["reason"],
    email=ticket.email  # Pipeline connector!
)
db.add(log)
db.commit()
```

---

## Summary

- **Pipeline = Connected stages** where each stage does one job
- **Email = Universal connector** that links all stages together
- **Stage 5 (our app) = Final stage** that decides if tickets need human escalation
- **Version 2 improvements = Pipeline integration** for better context and traceability

You now understand how your application fits into the bigger picture! 🎉
