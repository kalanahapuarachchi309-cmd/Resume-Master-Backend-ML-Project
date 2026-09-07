"""User Management Route Handlers."""
from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.schemas.auth import UserProfile
from app.core.security import require_role

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=List[UserProfile], dependencies=[Depends(require_role(["ADMIN"]))])
async def list_users(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    """List all registered users (Admin privilege required)."""
    # Stub: Member 1 to implement pagination and query
    pass


@router.get("/{user_id}", response_model=UserProfile)
async def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    """Fetch user profile by user ID."""
    # Stub: Member 1 to implement user query
    pass
