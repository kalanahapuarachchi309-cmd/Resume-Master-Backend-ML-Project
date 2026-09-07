"""Skill and Entity Extractor Service (Member 2 Focus)."""
from typing import List, Optional


class SkillExtractor:
    """Extracts technical skills, experience duration, and degrees from candidate text."""

    @staticmethod
    def extract_skills(text: str) -> List[str]:
        """Match and extract programming languages, frameworks, and tools from text."""
        # Stub: Member 2 to match against technical taxonomy dictionary
        pass

    @staticmethod
    def extract_experience_years(text: str) -> float:
        """Parse resume for numerical years of professional work experience."""
        # Stub: Member 2 to apply regex pattern matching for experience phrases
        pass

    @staticmethod
    def extract_education(text: str) -> Optional[str]:
        """Detect highest level of completed tertiary education (BSc, MSc, PhD, etc.)."""
        # Stub: Member 2 to detect academic degree designations
        pass
