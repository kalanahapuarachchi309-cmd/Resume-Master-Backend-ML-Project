# Resume-Master-Backend-ML-Project

> **AI-Powered Resume/CV Screening & Job Matching System**  
> An intelligent, end-to-end recruitment platform integrating FastAPI, PostgreSQL, and Machine Learning to automatically parse, evaluate, and rank candidate resumes against job specifications.

---

## 🏛️ System Architecture

The application follows the modular decoupled architecture required by the specification:

```
                      ┌────────────────────────────────────────┐
                      │            REACT FRONTEND              │
                      └──────────────────┬─────────────────────┘
                                         │ HTTP REST (JSON / Multipart)
                                         ▼
                      ┌────────────────────────────────────────┐
                      │          FASTAPI REST BACKEND          │
                      │  - JWT Authentication & RBAC           │
                      │  - Job Posting CRUD                    │
                      │  - Resume Upload & Parsing Gateway     │
                      └──────────────┬───────────────────┬─────┘
                                     │                   │
                        ORM Database │                   │ Feature Extraction
                                     ▼                   ▼
                      ┌──────────────────────┐   ┌────────────────────────────────┐
                      │      POSTGRESQL      │   │    ML PREDICTION SERVICE       │
                      │  - Users & Roles     │   │  - PDF / DOCX Text Extractors  │
                      │  - Jobs              │   │  - 6 Feature Engineering Steps │
                      │  - Resumes           │   │  - TF-IDF & Cosine Similarity  │
                      │  - Match Results     │   │  - Scikit-Learn Model & Vector │
                      └──────────────────────┘   └───────────────┬────────────────┘
                                                                 │
                                                                 ▼
                                                 ┌────────────────────────────────┐
                                                 │   RANKED EXPLAINABLE RESULTS   │
                                                 │  - Match Score (0–100%)        │
                                                 │  - Matched vs Missing Skills   │
                                                 │  - Experience & Education Fit  │
                                                 └────────────────────────────────┘
```

---

## 👥 Team Workload & Contribution Breakdown

This project backend is collaboratively engineered by 2 backend team members with distinct separation of concerns to ensure independent Git commit histories and comprehensive individual viva voce defense.

| Responsibilities | 👨💻 Member 1 (Core & Data) | 👨💻 Member 2 (ML & NLP) |
| :--- | :--- | :--- |
| **Primary Focus** | Backend Architecture, Auth, Database, Job APIs | Resume Parsing, NLP, Feature Engineering, ML Matching |
| **Assigned Files** | `app/main.py`, `app/core/`, `app/database/`, `app/models/`, `app/routes/auth.py`, `app/routes/jobs.py` | `app/services/parsers/`, `app/services/nlp/`, `app/services/feature_engineering.py`, `app/ml/`, `app/routes/resumes.py`, `app/routes/matching.py` |
| **Key Technologies** | FastAPI, SQLAlchemy, Alembic, PostgreSQL, PyJWT, Passlib (Bcrypt) | pdfplumber, python-docx, scikit-learn, NLTK/spaCy, Pandas, NumPy |
| **Viva Voce Defense** | DB normalisation, JWT stateless auth, RBAC security, API performance | NLP tokenization, 6 feature engineering techniques, TF-IDF vectorization, explainable ranking |

---

## ⚙️ Mandatory Feature Engineering Pipeline (Assignment Section 5)

Implemented in `app/services/feature_engineering.py`:

1. **Text Feature Extraction**: TF-IDF vectorization over resume text and target job descriptions.
2. **Feature Interaction & Overlap Ratio**: Jaccard index and weighted skill overlap:
   $$\text{Skill Overlap Ratio} = \frac{|\text{Resume Skills} \cap \text{Job Skills}|}{|\text{Job Skills}|}$$
3. **Domain Metric Engineering**: Experience delta calculation:
   $$\text{Experience Delta} = \text{Candidate Experience} - \text{Required Experience}$$
4. **Categorical Encoding**: Ordinal mapping of candidate educational degree level (`None: 0, Diploma: 1, Bachelor: 2, Master: 3, PhD: 4`).
5. **Missing Value Imputation**: Median/mode imputation for unmentioned resume attributes and fallback defaults.
6. **Normalization & Feature Scaling**: Min-Max scaling across composite match vectors to yield calibrated [0.0, 1.0] prediction inputs.

---

## 📂 Backend File Structure

```text
backend/
├── app/
│   ├── main.py                         # FastAPI application entrypoint, CORS, exception handlers
│   │
│   ├── core/
│   │   ├── config.py                   # Pydantic BaseSettings (.env loader)
│   │   └── security.py                 # JWT token generation, bcrypt password hashing, auth guards
│   │
│   ├── database/
│   │   ├── connection.py               # SQLAlchemy engine, session maker, get_db dependency
│   │   └── base.py                     # Base declarative class with model registry
│   │
│   ├── models/
│   │   ├── user.py                     # User table (roles: ADMIN, RECRUITER, CANDIDATE)
│   │   ├── job.py                      # Job table (title, description, required skills, exp)
│   │   ├── resume.py                   # Resume table (file path, raw text, parsed attributes)
│   │   └── match_result.py             # Match result table (job_id, resume_id, score, rank)
│   │
│   ├── schemas/
│   │   ├── auth.py                     # User registration, login, token DTOs
│   │   ├── job.py                      # Job creation, update, and response DTOs
│   │   ├── resume.py                   # Resume upload, parse status, and detail DTOs
│   │   └── matching.py                 # Evaluation request, candidate match detail, leaderboard DTOs
│   │
│   ├── routes/
│   │   ├── auth.py                     # POST /api/auth/register, POST /api/auth/login, GET /api/auth/me
│   │   ├── users.py                    # User profile and administrative management
│   │   ├── jobs.py                     # POST, GET, PUT, DELETE /api/jobs
│   │   ├── resumes.py                  # POST /api/resumes/upload, POST /api/resumes/upload-batch
│   │   └── matching.py                 # POST /api/matching/job/{id}/evaluate, GET /api/matching/job/{id}/rankings
│   │
│   ├── services/
│   │   ├── job_service.py              # Job business logic & filtering
│   │   ├── parsers/
│   │   │   ├── pdf_parser.py           # Multi-column PDF parsing via pdfplumber
│   │   │   └── docx_parser.py          # Word document parsing via python-docx
│   │   ├── nlp/
│   │   │   ├── cleaner.py              # Text cleaning, regex stripping, stopword removal
│   │   │   └── skill_extractor.py      # Technical skill taxonomy & experience regex extractor
│   │   ├── feature_engineering.py      # 6 core feature transformation methods
│   │   └── ranking_service.py          # Candidate scoring, ranking, and explainable breakdown
│   │
│   └── ml/
│       ├── predictor.py                # Model loader and inference execution wrapper
│       ├── model.pkl                   # Trained ML model artifact (scikit-learn)
│       └── vectorizer.pkl              # Pretrained TF-IDF vectorizer artifact
│
├── tests/
│   ├── test_auth.py                    # Authentication & authorization unit tests
│   └── test_ml_matching.py             # Feature engineering & parser unit tests
├── requirements.txt                    # Project dependencies
├── .env.example                        # Template environment variables
└── Dockerfile                          # Production container configuration
```

---

## 🚀 Quickstart & Installation

### 1. Prerequisites
- Python 3.10+
- PostgreSQL 14+
- Git

### 2. Setup Virtual Environment
```bash
# Clone the repository
git clone https://github.com/kalanahapuarachchi309-cmd/Resume-Master-Backend-ML-Project.git
cd Resume-Master-Backend-ML-Project/backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
.\venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Copy `.env.example` to `.env` and fill in credentials:
```bash
cp .env.example .env
```

### 4. Run Application
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

- **Interactive API Documentation (Swagger)**: `http://localhost:8000/docs`
- **ReDoc Documentation**: `http://localhost:8000/redoc`

---

## 🔒 API Endpoints Overview

| Method | Endpoint | Access | Description |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/auth/register` | Public | Register new candidate or recruiter |
| `POST` | `/api/auth/login` | Public | Authenticate user & return JWT token |
| `GET`  | `/api/auth/me` | Authenticated | Fetch current user session profile |
| `POST` | `/api/jobs` | Recruiter/Admin | Create a new job opening |
| `GET`  | `/api/jobs` | Public | List all jobs with skill/title filters |
| `GET`  | `/api/jobs/{id}` | Public | Retrieve detailed job specifications |
| `POST` | `/api/resumes/upload` | Candidate/Recruiter | Upload and parse single resume (.pdf/.docx) |
| `POST` | `/api/resumes/upload-batch`| Recruiter/Admin | Upload batch of resumes for evaluation |
| `POST` | `/api/matching/job/{id}/evaluate` | Recruiter/Admin | Run ML screening & scoring pipeline |
| `GET`  | `/api/matching/job/{id}/rankings` | Recruiter/Admin | Fetch ranked candidates with explainable insights |

---

## 📜 License
This project is developed for educational and academic evaluation purposes.
