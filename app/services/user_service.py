from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException, Depends
from app.core.supabase_bucket import supabase
import logging
from app.schemas import subjectCreate
from app.models import User, UserUsage
from app.Repository.Subject_Repo import list_subjects
from app.core.security import oauth2_scheme
from app.core.database import get_db

logger = logging.getLogger(__name__)


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> User:
    try:
        response = supabase.auth.get_user(token)
        auth_user = response.user

        if auth_user is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token.",
            )

        user = (
            db.query(User)
            .filter(User.id == auth_user.id)
            .options(joinedload(User.premium_type))
            .first()
        )

        if user is None:
            raise HTTPException(
                status_code=401,
                detail="User not found.",
            )

        return user

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token.",
        )


def login_user(token: str, db: Session):
    try:
        auth_user = supabase.auth.get_user(token).user

        if auth_user is None:
            raise HTTPException(status_code=404, detail="Invalid token.")

        user = db.query(User).filter(User.id == auth_user.id).first()

        if user is None:
            user = User(
                id=auth_user.id,
                email=auth_user.email,
                display_name=auth_user.user_metadata.get("full_name", ""),
                avatar_url=auth_user.user_metadata.get("avatar_url"),
                premium_type_id=1,
            )

            db.add(user)
            db.flush()  # Makes the user available before creating related rows

            usage = UserUsage(
                user_id=user.id,
                used_today=0,
            )

            db.add(usage)
            db.commit()
            db.refresh(user)

        return user

    except Exception as e:
        db.rollback()
        print(repr(e))
        raise
