from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import oauth2_scheme

router = APIRouter(prefix="/Login", tags=["Login"])
from app.services.user_service import login_user


@router.get("/")
@router.get("")
async def verify_auth(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    return login_user(token, db)
