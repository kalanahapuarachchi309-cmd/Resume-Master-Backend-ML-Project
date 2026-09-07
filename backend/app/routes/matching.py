"""ML Candidate Matching & Ranking Route Handlers (Member 2 Focus)."""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.schemas.matching import MatchEvaluationRequest, JobMatchingResponse
from app.core.security import require_role

router = APIRouter(prefix="/matching", tags=["Matching & Ranking"])


@router.post("/job/{job_id}/evaluate", response_model=JobMatchingResponse, status_code=status.HTTP_200_OK)
async def evaluate_candidates_for_job(
    job_id: int,
    request: MatchEvaluationRequest,
    current_user: dict = Depends(require_role(["RECRUITER", "ADMIN"])),
    db: Session = Depends(get_db),
):
    """Trigger ML feature extraction, scoring, and ranking for candidate resumes against job specifications."""
    # Stub: Member 2 to invoke feature engineering, predictor, and ranking service
    pass


@router.get("/job/{job_id}/rankings", response_model=JobMatchingResponse)
async def get_job_rankings(
    job_id: int,
    current_user: dict = Depends(require_role(["RECRUITER", "ADMIN"])),
    db: Session = Depends(get_db),
):
    """Retrieve saved ranking leaderboard and explainable match breakdown for a job."""
    # Stub: Member 2 / Member 1 to retrieve persisted match results
    pass
