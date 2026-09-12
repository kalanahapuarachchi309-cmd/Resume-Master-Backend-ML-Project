"""Candidate Ranking and Explainability Service Driven by Trained ML Model (Sampath & Team)."""
from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.job import Job
from app.models.resume import Resume
from app.models.match_result import MatchResult
from app.schemas.matching import CandidateMatchDetail, JobMatchingResponse
from app.services.feature_engineering import FeatureEngineeringPipeline
from app.ml.predictor import predictor_service


class RankingService:
    """Ranks candidates for a job opening using genuine ML model predictions and generates explainability reports."""

    @staticmethod
    def evaluate_candidates(
        db: Session,
        job_id: int,
        resume_ids: Optional[List[int]] = None
    ) -> JobMatchingResponse:
        """Evaluates candidate resumes against job vacancy specifications.

        Pipeline:
        1. Fetch Job and Candidate Resumes from database
        2. Extract identical 7 numerical features via FeatureEngineeringPipeline
        3. Predict match probability using the trained ML model (model.predict_proba)
        4. Sort candidates strictly descending by ML match score
        5. Assign ordinal ranks (1, 2, 3...)
        6. Prevent duplicate records by clearing prior rankings for this job
        7. Persist rankings to MatchResult table
        """
        job = db.query(Job).filter(Job.id == job_id).first()
        if not job:
            raise ValueError(f"Job with ID {job_id} not found")

        query = db.query(Resume)
        if resume_ids and len(resume_ids) > 0:
            query = query.filter(Resume.id.in_(resume_ids))
        resumes = query.all()

        if not resumes:
            return JobMatchingResponse(
                job_id=job.id,
                job_title=job.title,
                total_candidates_evaluated=0,
                evaluated_at=datetime.utcnow(),
                rankings=[],
            )

        evaluated_candidates = []

        for resume in resumes:
            # 1. Extract 7-feature vector & explainability data
            features, explain = FeatureEngineeringPipeline.extract_features(
                resume_text=resume.raw_text or "",
                job_description=job.description or "",
                candidate_skills=resume.parsed_skills or [],
                required_skills=job.required_skills or [],
                candidate_exp=resume.experience_years,
                required_exp=job.experience_required,
                candidate_edu=resume.education_level,
            )

            # 2. Get genuine ML predicted match probability from trained model
            ml_score = predictor_service.predict_match_probability(features)

            file_url = getattr(resume, "file_url", None) or (resume.file_path if resume.file_path and resume.file_path.startswith("http") else f"/api/resumes/{resume.id}/file")

            evaluated_candidates.append({
                "resume_id": resume.id,
                "candidate_name": resume.candidate_name or f"Candidate #{resume.id}",
                "match_score": ml_score,
                "matched_skills": explain["matched_skills"],
                "missing_skills": explain["missing_skills"],
                "experience_years": explain["experience_years"],
                "experience_fit": explain["experience_fit"],
                "file_url": file_url,
            })

        # 3. Sort candidates strictly descending by ML match score
        evaluated_candidates.sort(key=lambda c: c["match_score"], reverse=True)

        # 4. Clear prior evaluations for this job to prevent database duplicates
        db.query(MatchResult).filter(MatchResult.job_id == job.id).delete()
        db.commit()

        # 5. Assign ordinal rankings and persist to database
        rankings: List[CandidateMatchDetail] = []
        for idx, item in enumerate(evaluated_candidates, start=1):
            detail = CandidateMatchDetail(
                resume_id=item["resume_id"],
                candidate_name=item["candidate_name"],
                match_score=item["match_score"],
                rank=idx,
                matched_skills=item["matched_skills"],
                missing_skills=item["missing_skills"],
                experience_years=item["experience_years"],
                experience_fit=item["experience_fit"],
                file_url=item["file_url"],
            )
            rankings.append(detail)

            # Save in database
            record = MatchResult(
                job_id=job.id,
                resume_id=item["resume_id"],
                match_score=item["match_score"],
                rank=idx,
                matched_skills=item["matched_skills"],
                missing_skills=item["missing_skills"],
            )
            db.add(record)

        db.commit()

        return JobMatchingResponse(
            job_id=job.id,
            job_title=job.title,
            total_candidates_evaluated=len(rankings),
            evaluated_at=datetime.utcnow(),
            rankings=rankings,
        )

    @staticmethod
    def get_job_rankings(db: Session, job_id: int) -> JobMatchingResponse:
        """Fetch previously computed rankings for a job."""
        job = db.query(Job).filter(Job.id == job_id).first()
        if not job:
            raise ValueError(f"Job with ID {job_id} not found")

        records = (
            db.query(MatchResult, Resume)
            .join(Resume, MatchResult.resume_id == Resume.id)
            .filter(MatchResult.job_id == job_id)
            .order_by(MatchResult.rank.asc())
            .all()
        )

        rankings = []
        for match, resume in records:
            cand_exp = resume.experience_years or 0.0
            req_exp = job.experience_required or 0.0
            if cand_exp >= req_exp + 1.0:
                exp_fit = f"Exceeds Requirement (+{round(cand_exp - req_exp, 1)} yrs)"
            elif cand_exp >= req_exp:
                exp_fit = "Meets Requirement"
            else:
                exp_fit = f"Under Requirement (-{round(req_exp - cand_exp, 1)} yrs)"

            file_url = getattr(resume, "file_url", None) or (resume.file_path if resume.file_path and resume.file_path.startswith("http") else f"/api/resumes/{resume.id}/file")

            rankings.append(CandidateMatchDetail(
                resume_id=resume.id,
                candidate_name=resume.candidate_name or f"Candidate #{resume.id}",
                match_score=match.match_score,
                rank=match.rank,
                matched_skills=match.matched_skills or [],
                missing_skills=match.missing_skills or [],
                experience_years=cand_exp,
                experience_fit=exp_fit,
                file_url=file_url,
            ))

        return JobMatchingResponse(
            job_id=job.id,
            job_title=job.title,
            total_candidates_evaluated=len(rankings),
            evaluated_at=datetime.utcnow(),
            rankings=rankings,
        )
