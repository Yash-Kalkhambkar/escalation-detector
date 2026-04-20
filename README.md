# Escalation Detector — Pipeline Edition

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Stage 5 of a 5-stage B2B CRM pipeline. This FastAPI application performs LLM-based escalation detection on support tickets using the Groq API.

## 📚 Documentation

- **[Quick Start Guide](QUICKSTART.md)** - Get up and running in 3 steps
- **[Pipeline Explained](PIPELINE_EXPLAINED.md)** - Learn about the pipeline architecture and what's new in V2
- **[Architecture](ARCHITECTURE.md)** - System architecture, data flow, and technical diagrams
- **[Contributing](CONTRIBUTING.md)** - How to contribute to this project
- **[Changelog](CHANGELOG.md)** - Version history and updates

## Overview

The Escalation Detector reads support tickets from Stage 4 (Ticket Classifier), analyzes them using the llama-3.1-8b-instant model via Groq, and stores escalation decisions in the database. It provides both API endpoints and a web interface for interaction.

### Pipeline Context

- **Stage 1 (Leads)**: Initial lead capture and scoring
- **Stage 2 (Followups)**: Follow-up tracking and engagement
- **Stage 3 (Deals)**: Deal progression and conversation management
- **Stage 4 (Tickets)**: Support ticket classification and draft response generation
- **Stage 5 (Escalation Detector)**: Escalation analysis and decision logging (this application)

Customer email serves as the universal identifier across all stages.

## Technology Stack

- **FastAPI**: Web framework (synchronous endpoints)
- **SQLAlchemy**: ORM with PostgreSQL
- **psycopg2-binary**: PostgreSQL driver with SSL support
- **pydantic-settings**: Environment-based configuration
- **Groq Python SDK**: LLM service (llama-3.1-8b-instant)
- **Vanilla HTML/CSS/JS**: Frontend (no build tools)

## Installation

### 1. Clone and Setup Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Copy the example environment file and fill in your credentials:

```bash
cp .env.example .env
```

Edit `.env` with your actual values:

```env
DATABASE_URL=postgresql+psycopg2://user:password@host:port/database
GROQ_API_KEY=your_groq_api_key_here
```

**Getting API Keys:**
- **Groq API Key**: Sign up at [console.groq.com](https://console.groq.com/) and create an API key
- **Database URL**: Use your PostgreSQL connection string with SSL enabled

**Note**: The database tables already exist in the cloud database. No migration is needed.

### 4. Run the Application

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Escalation Endpoints

- **POST /escalation/check** - Manual escalation check with custom input
  - Body: `{"ticket_id": "string", "email": "string", "conversation": "string"}`
  - Returns: Escalation decision with reason

- **POST /escalation/from-ticket** - Pipeline-based escalation from ticket ID
  - Body: `{"ticket_id": integer}`
  - Returns: Escalation decision with enriched context from Stage 4

- **GET /escalation/logs** - Retrieve all escalation logs
  - Query param: `email` (optional) - Filter by customer email
  - Returns: List of escalation logs

- **GET /escalation/logs/ticket/{ticket_id}** - Get logs for specific ticket
  - Returns: All escalation checks for that ticket

- **GET /escalation/stats** - Get escalation statistics
  - Returns: Total, escalated, not_escalated, escalation_rate

- **GET /health** - Health check for database and LLM service
  - Returns: Status of database and LLM connections

### Pipeline Endpoints

- **GET /pipeline/trace/{email}** - Trace complete customer journey
  - Returns: All records across all 5 pipeline stages for the email

### Documentation

- **GET /docs** - Interactive API documentation (Swagger UI)
- **GET /redoc** - Alternative API documentation (ReDoc)

## Frontend Interface

Open `frontend/index.html` in a web browser to access the web interface.

### Features

1. **Pipeline Mode**: Submit a ticket ID from Stage 4 for automatic escalation check
2. **Manual Check**: Enter custom ticket information for escalation analysis
3. **Pipeline Trace**: View complete customer journey across all stages
4. **Recent Logs**: Auto-loading table of recent escalation decisions

## Project Structure

```
escalation-pipeline/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app, CORS, router inclusion
│   ├── config.py            # pydantic-settings configuration
│   ├── database.py          # SQLAlchemy engine and session
│   ├── models.py            # Database models (all 5 stages)
│   ├── schemas.py           # Pydantic request/response schemas
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── escalation.py    # Escalation endpoints
│   │   └── pipeline.py      # Pipeline trace endpoint
│   └── services/
│       ├── __init__.py
│       └── llm.py           # Groq API integration
├── frontend/
│   └── index.html           # Single-page web interface
├── .env                     # Environment variables (not in git)
├── .gitignore
├── requirements.txt
├── migrate.py               # Database migration script
└── README.md
```

## Database Tables

### escalation_logs (Read/Write)
- Stores escalation analysis results
- Fields: id, ticket_id, conversation, escalate, reason, email, created_at

### tickets (Read-Only - Stage 4)
- Support tickets from classifier
- Fields: id, text, email, category, urgency, status, draft_reply, created_at

### leads (Read-Only - Stage 1)
- Initial lead information
- Fields: id, name, company, description, score, score_reason, created_at

### followups (Read-Only - Stage 2)
- Follow-up tracking records
- Fields: id, prospect, last_interaction, days_since, email, created_at

### deals (Read-Only - Stage 3)
- Deal progression records
- Fields: id, prospect, conversation, stage, created_at

## How It Works

### Pipeline-Based Escalation

1. User submits a ticket ID from Stage 4
2. Application fetches ticket details from database
3. Constructs enriched context with category, urgency, status, text, and draft reply
4. Sends context to Groq API (llama-3.1-8b-instant)
5. LLM analyzes and returns escalation decision with reason
6. Stores result in escalation_logs table
7. Returns decision to user

### Manual Escalation

1. User provides ticket_id, email, and conversation text
2. Application sends conversation to Groq API
3. LLM analyzes and returns decision
4. Stores result in escalation_logs table
5. Returns decision to user

### Pipeline Trace

1. User provides customer email
2. Application queries all 5 pipeline stage tables
3. Aggregates results into complete customer journey
4. Returns timeline with all interactions

## Troubleshooting

### Database Connection Issues

- Verify DATABASE_URL in .env file
- Ensure SSL mode is set to "require"
- Check network connectivity to DigitalOcean database

### LLM Service Issues

- Verify GROQ_API_KEY in .env file
- Check Groq API status
- Review error messages in /health endpoint

### Frontend Not Loading Data

- Ensure backend is running on http://localhost:8000
- Check browser console for CORS errors
- Verify API endpoints are accessible

## Development

### Running in Development Mode

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Testing Endpoints

Use the interactive documentation at http://localhost:8000/docs to test all endpoints.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## Support

- 📖 [Documentation](PIPELINE_EXPLAINED.md)
- 🐛 [Report a Bug](https://github.com/Yash-Kalkhambkar/escalation-detector/issues)
- 💡 [Request a Feature](https://github.com/Yash-Kalkhambkar/escalation-detector/issues)

## Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- LLM powered by [Groq](https://groq.com/)
- Part of a 5-stage B2B CRM pipeline project
