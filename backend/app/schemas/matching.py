"""Candidate Evaluation and Job Matching Pydantic Schemas."""
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class MatchEvaluationRequest(BaseModel):
    """Payload to trigger matching evaluation for a specific job."""
    job_id: int
    resume_ids: Optional[List[int]] = None  # None evaluates all available resumes


class CandidateMatchDetail(BaseModel):
    """Granular explainable match result for an individual candidate."""
    resume_id: int
    candidate_name: str
    match_score: float = Field(..., ge=0.0, le=100.0, description="Percentage match score")
    rank: int
    matched_skills: List[str]
    missing_skills: List[str]
    experience_years: float
    experience_fit: str  # e.g., "Exceeds Requirement", "Meets Requirement", "Under Requirement"


class JobMatchingResponse(BaseModel):
    """Leaderboard summary response for a matched job posting."""
    job_id: int
    job_title: str
    total_candidates_evaluated: int
    evaluated_at: datetime
    rankings: List[CandidateMatchDetail]
