from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from contextlib import asynccontextmanager
import logging
import time
from .config import get_settings
from .database import init_db
from .routers import (
    projects_router,
    step1_router,
    step2_router,
    step3_router,
    step4_router
)
from .routers.drafts import router as drafts_router
from .routers.documents import router as documents_router
from .routers.downloads import router as downloads_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler (replaces deprecated @app.on_event)"""
    # Startup
    logger.info("Starting BFA Audit App...")
    try:
        init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down BFA Audit App...")


app = FastAPI(
    title="BFA Audit App",
    description="Comprehensive BFA automation audit application with AI-powered analysis",
    version="1.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Add processing time to response headers."""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    logger.info(f"{request.method} {request.url.path} - {response.status_code} - {process_time:.3f}s")
    return response


# Global exception handlers
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Handle HTTP exceptions with consistent format."""
    logger.error(f"HTTP error: {exc.status_code} - {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "message": exc.detail,
            "status_code": exc.status_code
        },
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors with detailed information."""
    logger.error(f"Validation error: {exc.errors()}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": True,
            "message": "Błąd walidacji danych",
            "details": exc.errors(),
            "status_code": 422
        },
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle unexpected errors gracefully."""
    logger.exception(f"Unexpected error: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": True,
            "message": "Wystąpił nieoczekiwany błąd. Spróbuj ponownie później.",
            "status_code": 500
        },
    )


# Include routers
app.include_router(projects_router)
app.include_router(drafts_router)
app.include_router(documents_router)
app.include_router(downloads_router)
app.include_router(step1_router)
app.include_router(step2_router)
app.include_router(step3_router)
app.include_router(step4_router)


@app.get("/", tags=["General"])
def root():
    """Root endpoint with API information."""
    return {
        "message": "BFA Audit App API",
        "version": "1.1.0",
        "description": "AI-powered BFA automation audit application",
        "features": [
            "Dynamic form generation with Claude Sonnet 4.5",
            "Extended Thinking analysis",
            "4-step audit framework",
            "Professional presentation generation"
        ],
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health", tags=["General"])
def health_check():
    """Health check endpoint with system status."""
    try:
        # Test database connection
        from .database import SessionLocal
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        db_status = "healthy"
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        db_status = "unhealthy"
    
    return {
        "status": "healthy" if db_status == "healthy" else "degraded",
        "version": "1.1.0",
        "database": db_status,
        "timestamp": time.time()
    }


@app.get("/api/config", tags=["General"])
def get_config():
    """Get public configuration information."""
    return {
        "claude_configured": bool(settings.claude_api_key),
        "gamma_configured": bool(settings.gamma_api_key),
        "features": {
            "dynamic_forms": True,
            "extended_thinking": True,
            "desktop_app": True
        }
    }
