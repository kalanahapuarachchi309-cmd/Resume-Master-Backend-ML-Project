"""FastAPI Application Entrypoint."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.routes.auth import router as auth_router
from app.routes.users import router as users_router
from app.routes.jobs import router as jobs_router
from app.routes.resumes import router as resumes_router
from app.routes.matching import router as matching_router

# Initialize FastAPI application
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    description="AI-Powered Resume Screening & Job Matching REST API",
    version="1.0.0",
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Routers under standard prefix
app.include_router(auth_router, prefix=settings.API_V1_STR)
app.include_router(users_router, prefix=settings.API_V1_STR)
app.include_router(jobs_router, prefix=settings.API_V1_STR)
app.include_router(resumes_router, prefix=settings.API_V1_STR)
app.include_router(matching_router, prefix=settings.API_V1_STR)


@app.get("/", tags=["Health"])
async def root():
    """Application root healthcheck."""
    return {
        "status": "online",
        "service": settings.PROJECT_NAME,
        "docs": "/docs",
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """System health check endpoint."""
    return {"status": "healthy"}
