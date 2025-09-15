import os
from enum import Enum
from typing import Any

from fastapi.security import HTTPBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import jwt

from sqlalchemy.orm import Session

from app.models import TokenBlacklist

# ---------------- PASSWORD HASHING ----------------
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# ---------------- JWT CONFIG ----------------
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS"))
UTC = timezone.utc


bearer_scheme = HTTPBearer()


class TokenType(str, Enum):
    ACCESS = "access"
    REFRESH = "refresh"


# ---------------- JWT UTIL ----------------
def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(UTC) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire, "token_type": TokenType.ACCESS})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict[str, Any], expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(UTC) + (expires_delta or timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))
    to_encode.update({"exp": expire, "token_type": TokenType.REFRESH})
    encoded_jwt: str = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# ---------------- BLACKLIST UTILS ----------------
def is_token_blacklisted(token: str, db: Session) -> bool:
    return db.query(TokenBlacklist).filter(TokenBlacklist.token == token).first() is not None


def blacklist_token(token: str, db: Session):
    db.add(TokenBlacklist(token=token))
    db.commit()