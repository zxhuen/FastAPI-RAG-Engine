from sqlalchemy.orm import Session
from fastapi import HTTPException, UploadFile, File
import logging
from app.core.supabase_bucket import supabase
from datetime import datetime, timedelta, UTC
from app.schemas import DocumentCreate, DocumentResponse
from app.Repository.Subject_Repo import list_subjects, find_subject_name
from app.models import Document

from uuid import UUID, uuid4

from app.core.status import DocumentStatus

from app.services.status_change import change_status
from app.core.status import DocumentStatus
from app.tasks.process_document_task import process_document
from app.models.User import User


def check_usage(user: User, text_length: str, db: Session):
    if datetime.now(UTC) - user.usage.last_reset_at >= timedelta(hours=24):
        user.usage.used_today = 0
        user.usage.last_reset_at = datetime.now(UTC)

    premium_limit = user.premium_type.daily_limit
    user_usage = user.usage.used_today + len(text_length)

    if user_usage > premium_limit:
        raise HTTPException(
            status_code=429,
            detail=(
                f"Daily usage limit exceeded. "
                f"Your plan allows up to {premium_limit} characters every 24 hours."
            ),
        )

    user.usage.used_today = user_usage

    return
