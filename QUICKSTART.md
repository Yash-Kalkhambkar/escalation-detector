# Quick Start Guide

## 🚀 Get Started in 3 Steps

### 1. Activate Virtual Environment

```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 2. Start the Server

```bash
uvicorn app.main:app --reload
```

The API will be available at: **http://localhost:8000**

### 3. Open the Frontend

Open `frontend/index.html` in your web browser.

## ✅ Verify Installation

Visit http://localhost:8000/escalation/health

Expected response:
```json
{
  "status": "healthy",
  "database": "connected",
  "llm": "operational"
}
```

## 📚 API Documentation

Interactive API docs: http://localhost:8000/docs

## 🎯 Quick Test

### Test Manual Escalation Check

```bash
curl -X POST http://localhost:8000/escalation/check \
  -H "Content-Type: application/json" \
  -d '{
    "ticket_id": "TEST-123",
    "email": "customer@example.com",
    "conversation": "I am very frustrated with your service and considering legal action"
  }'
```

### Test Pipeline-Based Check

```bash
curl -X POST http://localhost:8000/escalation/from-ticket \
  -H "Content-Type: application/json" \
  -d '{"ticket_id": 1}'
```

### View Statistics

```bash
curl http://localhost:8000/escalation/stats
```

### View Recent Logs

```bash
curl http://localhost:8000/escalation/logs
```

### Trace Customer Journey

```bash
curl http://localhost:8000/pipeline/trace/customer@example.com
```

## 🎨 Frontend Features

1. **Pipeline Mode**: Enter a ticket ID from Stage 4 for automatic escalation analysis
2. **Manual Check**: Submit custom ticket information for escalation analysis
3. **Pipeline Trace**: View complete customer journey across all 5 pipeline stages
4. **Recent Logs**: Auto-refreshing table of recent escalation decisions

## 🔧 Troubleshooting

### Server won't start
- Ensure virtual environment is activated
- Check that port 8000 is not in use
- Verify .env file exists with correct credentials

### Database connection issues
- Verify DATABASE_URL in .env file
- Check network connectivity
- Ensure SSL mode is set to "require"

### LLM service issues
- Verify GROQ_API_KEY in .env file
- Check Groq API status
- Review /escalation/health endpoint

## 📊 Current Status

The application is **fully functional** with:
- ✅ All API endpoints working
- ✅ Database connected
- ✅ LLM service operational
- ✅ Frontend interface ready
- ✅ CORS configured
- ✅ Health checks passing

## 🎯 Next Steps

1. Test the frontend by opening `frontend/index.html`
2. Try submitting a manual escalation check
3. Test pipeline-based escalation with existing ticket IDs
4. View the pipeline trace for a customer email
5. Explore the API documentation at /docs

Enjoy using the Escalation Detector! 🚀
