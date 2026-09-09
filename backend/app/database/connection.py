"""Database Engine and Session Management (Kalana)."""
import os
import logging
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from app.core.config import settings

logger = logging.getLogger(__name__)

# Determine database engine with automatic SQLite fallback
database_url = settings.DATABASE_URL

if database_url.startswith("sqlite"):
    engine = create_engine(
        database_url,
        connect_args={"check_same_thread": False}
    )
else:
    try:
        engine = create_engine(database_url, pool_pre_ping=True)
    except Exception as e:
        logger.warning(f"Could not initialize PostgreSQL engine ({e}). Falling back to local SQLite.")
        fallback_url = "sqlite:///./resume_matcher.db"
        engine = create_engine(fallback_url, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """Dependency for obtaining a scoped database session per request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initializes all database tables on application startup."""
    import app.models  # Ensure all ORM models are registered with Base metadata
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables initialized successfully.")
