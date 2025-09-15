from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app import crud, schemas
from app.dependencies import get_current_user
from app.schemas import UserOutSchema

router = APIRouter()


@router.post("/", response_model=schemas.UserOutSchema)
def register_user(user: schemas.UserCreateSchema, db: Session = Depends(get_db)):
    return crud.create_user(db, user)


@router.get("/", response_model=List[schemas.UserOutSchema])
def read_users(db: Session = Depends(get_db)):
    return crud.get_users(db)


@router.get("/me", response_model=schemas.UserOutSchema)
async def read_users_me(current_user: UserOutSchema = Depends(get_current_user)):
    return current_user