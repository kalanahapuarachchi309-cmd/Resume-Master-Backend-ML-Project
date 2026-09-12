"""Resume Upload, File Ingestion, and Batch Parsing Handlers (Mahen & Team)."""
import os
import uuid
import re
from typing import List
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.database.connection import get_db
from app.models.user import User
from app.models.resume import Resume
from app.schemas.resume import ResumeUploadResponse, ResumeDetailResponse
from app.services.parsers.pdf_parser import PDFParser
from app.services.parsers.docx_parser import DocxParser
from app.services.nlp.skill_extractor import SkillExtractor
from app.core.security import get_current_user

router = APIRouter(prefix="/resumes", tags=["Resumes"])


def _save_and_parse_file(file_bytes: bytes, original_filename: str) -> dict:
    """Helper to validate, save to unique path, and parse document."""
    # Enforce file size limit
    max_bytes = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024
    if len(file_bytes) > max_bytes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File exceeds maximum allowed size of {settings.MAX_UPLOAD_SIZE_MB}MB"
        )

    # Sanitize and create unique file storage path
    clean_name = re.sub(r"[^a-zA-Z0-9_\.-]", "_", original_filename.lower())
    ext = os.path.splitext(clean_name)[1]
    if ext not in [".pdf", ".docx"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported file format. Please upload .pdf or .docx files only."
        )

    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    unique_filename = f"{uuid.uuid4().hex[:10]}_{clean_name}"
    disk_path = os.path.join(settings.UPLOAD_DIR, unique_filename)

    # Write actual file bytes to disk
    with open(disk_path, "wb") as f:
        f.write(file_bytes)

    # Extract text according to format
    if ext == ".pdf":
        if not PDFParser.validate_file(file_bytes):
            raise HTTPException(status_code=400, detail="Uploaded file is not a valid PDF document.")
        raw_text = PDFParser.extract_text(file_bytes)
    else:  # .docx
        if not DocxParser.validate_file(file_bytes):
            raise HTTPException(status_code=400, detail="Uploaded file is not a valid DOCX document.")
        raw_text = DocxParser.extract_text(file_bytes)

    if not raw_text or len(raw_text.strip()) < 20:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not extract readable text from resume. Please ensure the document is not an empty or scanned image file."
        )

    # NLP feature extraction
    parsed_skills = SkillExtractor.extract_skills(raw_text)
    experience_years = SkillExtractor.extract_experience_years(raw_text)
    education_level = SkillExtractor.extract_education(raw_text)

    return {
        "filename": original_filename,
        "file_path": disk_path,
        "raw_text": raw_text,
        "parsed_skills": parsed_skills,
        "experience_years": experience_years,
        "education_level": education_level,
    }


@router.post("/upload", response_model=ResumeUploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_resume(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Upload and parse an individual candidate resume (.pdf or .docx)."""
    content = await file.read()
    parsed_data = _save_and_parse_file(content, file.filename)

    resume = Resume(
        candidate_id=current_user.id,
        candidate_name=current_user.name,
        filename=parsed_data["filename"],
        file_path=parsed_data["file_path"],
        raw_text=parsed_data["raw_text"],
        parsed_skills=parsed_data["parsed_skills"],
        experience_years=parsed_data["experience_years"],
        education_level=parsed_data["education_level"],
    )
    db.add(resume)
    db.commit()
    db.refresh(resume)

    return ResumeUploadResponse(
        id=resume.id,
        filename=resume.filename,
        candidate_name=resume.candidate_name,
        parsed_skills=resume.parsed_skills,
        experience_years=resume.experience_years,
        education_level=resume.education_level,
        uploaded_at=resume.uploaded_at,
        message="Resume successfully processed and indexed.",
    )


@router.post("/upload-batch", response_model=List[ResumeUploadResponse], status_code=status.HTTP_201_CREATED)
@router.post("/upload-bulk", response_model=List[ResumeUploadResponse], status_code=status.HTTP_201_CREATED)
async def upload_batch_resumes(
    files: List[UploadFile] = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Upload and parse a batch/bulk of candidate resumes simultaneously."""
    if not files or len(files) == 0:
        raise HTTPException(status_code=400, detail="No files were provided for upload.")

    results = []
    for upload in files:
        try:
            content = await upload.read()
            parsed_data = _save_and_parse_file(content, upload.filename)

            # Generate clean candidate name from filename
            base_name = upload.filename.rsplit(".", 1)[0]
            clean_name = re.sub(r"(?i)(_resume|_cv|resume|cv)", "", base_name).strip(" _-")
            candidate_display_name = clean_name.replace("_", " ").replace("-", " ").title()
            if not candidate_display_name:
                candidate_display_name = base_name.replace("_", " ").title()

            resume = Resume(
                candidate_id=current_user.id,
                candidate_name=candidate_display_name,
                filename=parsed_data["filename"],
                file_path=parsed_data["file_path"],
                raw_text=parsed_data["raw_text"],
                parsed_skills=parsed_data["parsed_skills"],
                experience_years=parsed_data["experience_years"],
                education_level=parsed_data["education_level"],
            )
            db.add(resume)
            db.commit()
            db.refresh(resume)

            results.append(ResumeUploadResponse(
                id=resume.id,
                filename=resume.filename,
                candidate_name=resume.candidate_name,
                parsed_skills=resume.parsed_skills,
                experience_years=resume.experience_years,
                education_level=resume.education_level,
                uploaded_at=resume.uploaded_at,
                message="Successfully parsed and indexed.",
            ))
        except Exception as e:
            # Continue with other files if one file fails
            continue

    return results


@router.get("/", response_model=List[ResumeDetailResponse])
def list_resumes(
    skip: int = 0,
    limit: int = 50,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List parsed candidate resumes. Candidates view their own; Recruiters view all."""
    query = db.query(Resume)
    user_role = current_user.role.value if hasattr(current_user.role, "value") else str(current_user.role)

    if user_role == "CANDIDATE":
        query = query.filter(Resume.candidate_id == current_user.id)

    return query.order_by(Resume.uploaded_at.desc()).offset(skip).limit(limit).all()


@router.get("/{resume_id}", response_model=ResumeDetailResponse)
def get_resume(
    resume_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retrieve detailed parsed resume data."""
    resume = db.query(Resume).filter(Resume.id == resume_id).first()
    if not resume:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resume not found")

    user_role = current_user.role.value if hasattr(current_user.role, "value") else str(current_user.role)
    if user_role == "CANDIDATE" and resume.candidate_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied to candidate record")

    return resume
