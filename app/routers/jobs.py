from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import crud, schemas


router = APIRouter()


@router.post("/", response_model=schemas.JobOut)
def create_job(job: schemas.JobCreate, db: Session = Depends(get_db)):
    return crud.create_job(db, job)


@router.get("/", response_model=List[schemas.JobOut])
def read_jobs(db: Session = Depends(get_db)):
    return crud.get_jobs(db)
