from sqlalchemy.orm import Session
import logging  
from app.schemas import subjectCreate
from app.models import Subject
from app.Repository.Subject_Repo import list_subjects

logger = logging.getLogger(__name__)

def create_subject(subject: subjectCreate, db: Session):
    new_subject = Subject(
        name = subject.name,
        term = subject.term
    )

    db.add(new_subject)
    db.commit()
    db.refresh(new_subject)

    return new_subject

def list_all_subject(db: Session):
    return list_subjects(db)



