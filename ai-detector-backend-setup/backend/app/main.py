"""
AI Crop Disease Detector - FastAPI Backend
Main application entry point
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.database import engine, Base
from app.routers import auth, predictions
from app.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create database tables
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created")
    yield
    # Shutdown
    print("👋 Shutting down...")


app = FastAPI(
    title="AI Crop Disease Detector API",
    description="Backend API for crop disease detection using AI",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(predictions.router, prefix="/api/predictions", tags=["Predictions"])


@app.get("/")
async def root():
    return {"message": "AI Crop Disease Detector API", "status": "running"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
