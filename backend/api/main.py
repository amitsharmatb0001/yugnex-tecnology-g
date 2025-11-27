"""
FILE: main.py
PATH: yugnex/backend/api/main.py
PURPOSE: The entry point for the FastAPI application.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.settings import settings
from api.routes import auth, chat, projects, agents

# Initialize App
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="YugNex AI Agency Backend API"
)

# CORS (Cross-Origin Resource Sharing)
origins = [
    "http://localhost:5173",  # Vite default
    "http://localhost:3000",  # React default
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
# FIX: 'auth', 'projects', etc. are already APIRouter instances.
# We include them with the "/api" prefix.
# Since the routers themselves define prefixes (e.g., "/auth"), 
# the final URL will be "/api/auth/login", "/api/projects/", etc.

app.include_router(auth, prefix="/api")
app.include_router(projects, prefix="/api")
app.include_router(chat, prefix="/api")
app.include_router(agents, prefix="/api")

# Root Endpoint (Health Check)
@app.get("/health")
async def health_check():
    """
    PURPOSE: Simple health check endpoint.
    """
    return {"status": "ok", "version": settings.APP_VERSION, "app": settings.APP_NAME}

# Startup Event
@app.on_event("startup")
async def startup_db_client():
    pass

@app.on_event("shutdown")
async def shutdown_db_client():
    pass