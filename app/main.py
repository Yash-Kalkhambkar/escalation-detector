from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.routers import escalation, pipeline

# Create tables (checkfirst=True prevents errors if tables exist)
Base.metadata.create_all(bind=engine, checkfirst=True)

app = FastAPI(
    title="Escalation Detector — Pipeline Edition",
    version="2.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Include routers
app.include_router(escalation.router, prefix="/escalation", tags=["Escalation"])
app.include_router(pipeline.router, prefix="/pipeline", tags=["Pipeline"])


@app.get("/")
def root():
    return {
        "message": "Welcome to Escalation Detector — Pipeline Edition (Stage 5)",
        "version": "2.0",
        "docs": "/docs"
    }
