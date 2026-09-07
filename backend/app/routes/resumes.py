"""Resume Upload and Ingestion Route Handlers (Member 2 Focus)."""
from typing import List
from fastapi import APIRouter, Depends, UploadFile, File, status
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.schemas.resume import ResumeUploadResponse, ResumeDetailResponse
from app.core.security import get_current_user

router = APIRouter(prefix="/resumes", tags=["Resumes"])


@router.post("/upload", response_model=ResumeUploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_resume(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Upload and parse an individual candidate resume (.pdf or .docx)."""
    # Stub: Member 2 to invoke pdf_parser/docx_parser, extract text & skills, and store in DB
    pass


@router.post("/upload-batch", response_model=List[ResumeUploadResponse], status_code=status.HTTP_201_CREATED)
async def upload_batch_resumes(
    files: List[UploadFile] = File(...),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Upload and parse a batch of resumes simultaneously."""
    # Stub: Member 2 to iterate, parse, and ingest batch files
    pass


@router.get("/", response_model=List[ResumeDetailResponse])
async def list_resumes(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    """List parsed resumes with pagination."""
    # Stub: Fetch stored resumes
    pass


@router.get("/{resume_id}", response_model=ResumeDetailResponse)
async def get_resume(resume_id: int, db: Session = Depends(get_db)):
    """Retrieve full parsed data and raw text for a specific resume."""
    # Stub: Fetch single resume record
    pass
