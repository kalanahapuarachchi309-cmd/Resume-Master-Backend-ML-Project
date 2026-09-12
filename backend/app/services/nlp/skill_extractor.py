"""Skill, Experience, and Education Extractor with Normalization (Mahen & Team)."""
import re
from datetime import datetime
from typing import List, Optional, Tuple

# Technical skill taxonomy with canonical mappings
SKILL_ALIASES = {
    # Languages
    "js": "JavaScript",
    "javascript": "JavaScript",
    "ts": "TypeScript",
    "typescript": "TypeScript",
    "python": "Python",
    "py": "Python",
    "java": "Java",
    "c++": "C++",
    "cpp": "C++",
    "c#": "C#",
    "golang": "Go",
    "go": "Go",
    "rust": "Rust",
    "php": "PHP",
    "ruby": "Ruby",
    "swift": "Swift",
    "kotlin": "Kotlin",
    
    # Frameworks & Libraries
    "react": "React",
    "reactjs": "React",
    "react.js": "React",
    "angular": "Angular",
    "vue": "Vue",
    "vue.js": "Vue",
    "vuejs": "Vue",
    "next.js": "Next.js",
    "nextjs": "Next.js",
    "node": "Node.js",
    "nodejs": "Node.js",
    "node.js": "Node.js",
    "express": "Express",
    "express.js": "Express",
    "django": "Django",
    "flask": "Flask",
    "fastapi": "FastAPI",
    "spring": "Spring Boot",
    "spring boot": "Spring Boot",
    "laravel": "Laravel",
    "dotnet": ".NET",
    ".net": ".NET",

    # Databases
    "sql": "SQL",
    "postgresql": "PostgreSQL",
    "postgres": "PostgreSQL",
    "mysql": "MySQL",
    "mongodb": "MongoDB",
    "mongo": "MongoDB",
    "redis": "Redis",
    "elasticsearch": "Elasticsearch",
    "sqlite": "SQLite",
    "oracle": "Oracle",

    # Cloud & DevOps
    "docker": "Docker",
    "kubernetes": "Kubernetes",
    "k8s": "Kubernetes",
    "aws": "AWS",
    "amazon web services": "AWS",
    "azure": "Azure",
    "gcp": "GCP",
    "google cloud": "GCP",
    "ci/cd": "CI/CD",
    "cicd": "CI/CD",
    "terraform": "Terraform",
    "ansible": "Ansible",
    "linux": "Linux",
    "git": "Git",
    "github": "Git",
    "gitlab": "Git",
    "jenkins": "Jenkins",

    # AI / ML / Data
    "machine learning": "Machine Learning",
    "ml": "Machine Learning",
    "deep learning": "Deep Learning",
    "dl": "Deep Learning",
    "nlp": "NLP",
    "natural language processing": "NLP",
    "computer vision": "Computer Vision",
    "cv": "Computer Vision",
    "pytorch": "PyTorch",
    "tensorflow": "TensorFlow",
    "scikit-learn": "Scikit-Learn",
    "sklearn": "Scikit-Learn",
    "pandas": "Pandas",
    "numpy": "NumPy",
    "power bi": "Power BI",
    "tableau": "Tableau",
    "data analysis": "Data Analysis",

    # Web & Architecture
    "html": "HTML",
    "html5": "HTML",
    "css": "CSS",
    "css3": "CSS",
    "tailwind": "Tailwind CSS",
    "tailwind css": "Tailwind CSS",
    "bootstrap": "Bootstrap",
    "rest": "REST API",
    "rest api": "REST API",
    "restful": "REST API",
    "graphql": "GraphQL",
    "microservices": "Microservices",
    "selenium": "Selenium",
    "pytest": "Pytest",
}


class SkillExtractor:
    """Extracts normalized technical skills, experience duration, and degrees."""

    @staticmethod
    def extract_skills(text: str) -> List[str]:
        """Match and normalize programming languages, frameworks, and tools."""
        if not text:
            return []

        text_lower = f" {text.lower()} "
        found_skills = set()

        # Sort alias keys by length descending to match multi-word phrases first
        sorted_aliases = sorted(SKILL_ALIASES.keys(), key=lambda x: len(x), reverse=True)

        for alias in sorted_aliases:
            pattern = rf"(?:\b|\s){re.escape(alias)}(?:\b|\s|[,\.;])"
            if re.search(pattern, text_lower):
                canonical = SKILL_ALIASES[alias]
                found_skills.add(canonical)

        return sorted(list(found_skills))

    @staticmethod
    def extract_experience_years(text: str) -> float:
        """Parse resume for professional work experience using regex & date spans."""
        if not text:
            return 0.0

        # Pattern 1: Explicit statements ("5+ years of experience", "worked for 4 years")
        explicit_patterns = [
            r"(\d+(?:\.\d+)?)\+?\s*(?:years?|yrs?)(?:\s+of)?\s+(?:professional\s+)?experience",
            r"experience\s*:\s*(\d+(?:\.\d+)?)\s*(?:years?|yrs?)",
            r"worked\s+(?:for\s+)?(\d+(?:\.\d+)?)\s*(?:years?|yrs?)",
            r"over\s+(\d+(?:\.\d+)?)\s*(?:years?|yrs?)(?:\s+of)?\s+experience",
        ]

        for pat in explicit_patterns:
            match = re.search(pat, text, re.IGNORECASE)
            if match:
                try:
                    exp = float(match.group(1))
                    if 0.5 <= exp <= 35.0:
                        return exp
                except ValueError:
                    pass

        # Pattern 2: Year date ranges (e.g., 2019 - 2024, 2021 - Present)
        current_year = datetime.now().year
        year_matches = re.findall(r"\b(20\d\d|19\d\d)\s*(?:-|–|to)\s*(20\d\d|present|current)\b", text, re.IGNORECASE)
        total_range_years = 0.0

        for start_str, end_str in year_matches:
            try:
                start_y = int(start_str)
                end_y = current_year if end_str.lower() in ["present", "current"] else int(end_str)
                diff = max(0, end_y - start_y)
                if diff <= 25:
                    total_range_years += diff
            except ValueError:
                pass

        if total_range_years > 0.0:
            return min(30.0, total_range_years)

        return 0.0

    @staticmethod
    def extract_education(text: str) -> str:
        """Detect highest level of completed tertiary education."""
        if not text:
            return "None"

        text_lower = text.lower()
        if re.search(r"\b(ph\.?d|doctor of philosophy|doctorate)\b", text_lower):
            return "PhD"
        if re.search(r"\b(master|msc|m\.sc|m\.tech|mba|meng)\b", text_lower):
            return "MSc"
        if re.search(r"\b(bachelor|bsc|b\.sc|b\.e|b\.tech|beng|bba|undergraduate)\b", text_lower):
            return "Bachelor"
        if re.search(r"\b(diploma|associate|higher diploma)\b", text_lower):
            return "Diploma"

        return "None"
