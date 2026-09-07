"""Job Posting Pydantic Schemas."""
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class JobBase(BaseModel):
    """Base schema for job properties."""
    title: str = Field(..., min_length=3, max_length=255)
    description: str = Field(..., min_length=10)
    required_skills: List[str] = Field(default_factory=list)
    experience_required: float = Field(default=0.0, ge=0.0)
    location: Optional[str] = None


class JobCreate(JobBase):
    """Schema for creating a new job posting."""
    pass


class JobUpdate(BaseModel):
    """Schema for updating an existing job posting."""
    title: Optional[str] = None
    description: Optional[str] = None
    required_skills: Optional[List[str]] = None
    experience_required: Optional[float] = None
    location: Optional[str] = None


class JobResponse(JobBase):
    """Schema for serializing a job posting in API responses."""
    id: int
    recruiter_id: int
    created_at: datetime

    class Config:
        from_attributes = True
