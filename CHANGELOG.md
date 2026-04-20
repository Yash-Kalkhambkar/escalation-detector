# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2024-01-15

### Added - Pipeline Edition
- **Pipeline Integration**: Full integration with 5-stage B2B CRM pipeline
- **From-Ticket Endpoint**: New `POST /escalation/from-ticket` endpoint that reads directly from Stage 4 tickets table
- **Pipeline Trace**: New `GET /pipeline/trace/{email}` endpoint showing complete customer journey across all 5 stages
- **Email-Based Filtering**: Filter escalation logs by customer email
- **Enriched Context**: AI now receives ticket category, urgency, status, and draft reply for better decisions
- **Read-Only Models**: Added models for leads, followups, deals, and tickets tables
- **Pipeline Documentation**: Added PIPELINE_EXPLAINED.md with comprehensive pipeline education
- **Frontend Pipeline Mode**: New section in UI for pipeline-based escalation checks
- **Frontend Pipeline Trace**: New section showing customer journey timeline

### Changed
- **Database Models**: Added email field to EscalationLog for pipeline traceability
- **LLM Context**: Enhanced context sent to AI with structured ticket metadata
- **Frontend UI**: Reorganized into 4 sections (Pipeline Mode, Manual Check, Pipeline Trace, Recent Logs)
- **API Response**: Added email field to all escalation responses
- **Health Check**: Now verifies both database and LLM service connectivity

### Improved
- **Decision Quality**: AI makes better escalation decisions with enriched context
- **Traceability**: Complete customer journey tracking via email identifier
- **User Experience**: Clearer separation between pipeline and manual modes
- **Documentation**: More comprehensive README and new educational materials

## [1.0.0] - 2024-01-01

### Added - Initial Release
- **Manual Check Endpoint**: `POST /escalation/check` for custom ticket analysis
- **Logs Retrieval**: `GET /escalation/logs` to view all escalation decisions
- **Ticket Logs**: `GET /escalation/logs/ticket/{ticket_id}` for ticket-specific logs
- **Statistics**: `GET /escalation/stats` for escalation metrics
- **Health Check**: `GET /health` for service status
- **LLM Integration**: Groq API integration with llama-3.1-8b-instant model
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Frontend**: Single-page HTML interface with manual check form
- **Configuration**: Environment-based configuration with pydantic-settings
- **CORS**: Enabled for frontend integration
- **Documentation**: Basic README and setup instructions

### Technical Stack
- FastAPI (synchronous)
- SQLAlchemy with psycopg2-binary
- Groq Python SDK
- Vanilla HTML/CSS/JavaScript
- PostgreSQL with SSL

---

## Version Comparison

### What's New in V2 (Pipeline Edition)?

**V1 (Standalone):**
- Manual ticket input only
- No integration with other systems
- Basic escalation analysis
- Single-purpose application

**V2 (Pipeline Edition):**
- ✅ Integrated with 5-stage CRM pipeline
- ✅ Automatic ticket fetching from Stage 4
- ✅ Complete customer journey tracking
- ✅ Enriched AI context with ticket metadata
- ✅ Email-based filtering and tracing
- ✅ Read-only access to all pipeline stages
- ✅ Enhanced frontend with pipeline visualization

---

## Upgrade Guide (V1 → V2)

### Database Changes
1. Add `email` column to `escalation_logs` table (nullable for backward compatibility)
2. No changes to existing data required

### API Changes
- All existing V1 endpoints remain functional
- New endpoints added (backward compatible)
- Response schemas extended with email field

### Configuration Changes
- No changes to `.env` file required
- Same DATABASE_URL and GROQ_API_KEY

### Frontend Changes
- V1 manual check functionality preserved
- New pipeline mode added
- Existing bookmarks/links still work

---

## Future Roadmap

### Planned for V2.1
- [ ] Bulk escalation checks
- [ ] Webhook notifications
- [ ] Advanced filtering options
- [ ] Export functionality

### Planned for V3.0
- [ ] Authentication and authorization
- [ ] Role-based access control
- [ ] Real-time escalation alerts
- [ ] Machine learning model training
- [ ] Custom escalation rules engine

---

## Support

For questions or issues, please open a GitHub issue or refer to the documentation:
- README.md - Setup and usage
- PIPELINE_EXPLAINED.md - Pipeline architecture
- QUICKSTART.md - Quick start guide
