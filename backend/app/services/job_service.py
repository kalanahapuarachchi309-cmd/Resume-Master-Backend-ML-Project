"""Job Management Service Layer (Kalana)."""
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.job import Job
from app.schemas.job import JobCreate, JobUpdate


class JobService:
    @staticmethod
    def get_job(db: Session, job_id: int) -> Optional[Job]:
        return db.query(Job).filter(Job.id == job_id).first()

    @staticmethod
    def list_jobs(db: Session, skip: int = 0, limit: int = 50, search: Optional[str] = None) -> List[Job]:
        query = db.query(Job)
        if search and search.strip():
            keyword = f"%{search.strip()}%"
            query = query.filter(
                (Job.title.ilike(keyword)) | 
                (Job.description.ilike(keyword)) |
                (Job.location.ilike(keyword))
            )
        return query.order_by(Job.created_at.desc()).offset(skip).limit(limit).all()

    @staticmethod
    def create_job(db: Session, job_in: JobCreate, recruiter_id: int) -> Job:
        job = Job(
            recruiter_id=recruiter_id,
            title=job_in.title,
            description=job_in.description,
            required_skills=job_in.required_skills,
            experience_required=job_in.experience_required,
            location=job_in.location,
        )
        db.add(job)
        db.commit()
        db.refresh(job)
        return job
