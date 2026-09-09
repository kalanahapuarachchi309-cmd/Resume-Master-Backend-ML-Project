"""Database Engine and Session Management (Kalana)."""
import os
import logging
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from app.core.config import settings

logger = logging.getLogger(__name__)
database_url = settings.DATABASE_URL
engine = create_engine(database_url if database_url.startswith("sqlite") else "sqlite:///./resume_matcher.db")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
