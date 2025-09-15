from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import crud, schemas


router = APIRouter()


@router.post("/", response_model=schemas.JobOutSchema)
def create_job(job: schemas.JobCreateSchema, db: Session = Depends(get_db)):
    return crud.create_job(db, job)


@router.get("/", response_model=List[schemas.JobOutSchema])
def read_jobs(db: Session = Depends(get_db)):
    return crud.get_jobs(db)
