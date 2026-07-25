from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import oauth2_scheme
from app.services.user_service import get_current_user
from app.schemas.user import UserResponse
router = APIRouter(prefix="/User", tags=["User"])
from app.services.user_service import login_user

@router.get("/get-current-user", response_model=UserResponse)
async def get_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    return get_current_user(token, db)