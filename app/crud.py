from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models import User, Job
from app.schemas import JobCreateSchema, UserCreateSchema
from app.utils import hash_password, verify_password


# Users
def create_user(db: Session, user: UserCreateSchema) -> User:
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    db_user = User(
        username=user.username,
        email=str(user.email),
        full_name=user.full_name,
        hashed_password=hash_password(user.password)
    )
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except Exception:
        db.rollback()
        raise
    return db_user


def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_users(db: Session):
    return db.query(User).all()


# Jobs
def create_job(db: Session, job: JobCreateSchema):
    db_job = Job(title=job.title, description=job.description)
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

def get_jobs(db: Session):
    return db.query(Job).all()
