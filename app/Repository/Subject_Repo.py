from sqlalchemy.orm import Session
from app.models import Subject

def list_subjects(db: Session):
    return db.query(Subject).all()

def find_subject_name(name: str, db: Session):
    return db.query(Subject).filter(Subject.name == name).first()

