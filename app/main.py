"""Main FastAPI application entry point"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import copilot

app = FastAPI(
    title="Restaurant Copilot API",
    description="AI-powered copilot for restaurants and internal Restaurant teams",
    version="0.1.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(copilot.router)


@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Restaurant Copilot API"}


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}
