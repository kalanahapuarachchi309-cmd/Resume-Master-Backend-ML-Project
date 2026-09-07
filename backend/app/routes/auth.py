"""Authentication Route Handlers (Member 1 Focus)."""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.schemas.auth import UserRegister, UserLogin, TokenResponse, UserProfile
from app.core.security import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserProfile, status_code=status.HTTP_201_CREATED)
async def register(user_in: UserRegister, db: Session = Depends(get_db)):
    """Register a new candidate or recruiter account."""
    # Stub: Member 1 to implement email uniqueness check, password hashing, and DB save
    pass


@router.post("/login", response_model=TokenResponse)
async def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """Authenticate user with email/password and issue a JWT bearer token."""
    # Stub: Member 1 to implement credential verification and token generation
    pass


@router.get("/me", response_model=UserProfile)
async def get_me(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    """Retrieve currently authenticated user profile."""
    # Stub: Member 1 to fetch full profile details from DB
    pass
