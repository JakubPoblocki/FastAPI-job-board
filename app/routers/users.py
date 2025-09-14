from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import crud, schemas
from app.dependencies import get_current_user
from app.models import User
from app.schemas import UserOut

router = APIRouter()

@router.post("/", response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    return crud.create_user(db, user)


@router.get("/", response_model=List[schemas.UserOut])
def read_users(db: Session = Depends(get_db)):
    return crud.get_users(db)

@router.get("/me", response_model=schemas.UserOut)
async def read_users_me(current_user: UserOut = Depends(get_current_user)):
    return current_user