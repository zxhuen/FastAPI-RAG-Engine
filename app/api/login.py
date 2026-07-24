from fastapi import Depends, APIRouter
from app.core.security import oauth2_scheme

router = APIRouter(prefix="/Login", tags=["Login"])

@router.get("")
async def verify_auth(token: str = Depends(oauth2_scheme)):
    print("hi")