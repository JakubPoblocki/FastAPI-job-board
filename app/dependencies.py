from typing import Any, Coroutine, Type

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from jose import JWTError, jwt
from app.database import get_db
from app.models import User
from app.utils import SECRET_KEY, ALGORITHM, is_token_blacklisted, TokenType

from sqlalchemy.orm import Session


bearer_scheme = HTTPBearer()


# ---------------- USER DEPENDENCIES ----------------
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db)
) -> User:
    """Dependency to get the current user from the token.
    Raises HTTPException if the token is invalid or the user does not exist.
    Used for routes that require authentication.

    :param credentials: HTTPAuthorizationCredentials object.
    :param db: Database session.
    :return: User object.
    """
    token = credentials.credentials
    if is_token_blacklisted(token, db):
        raise HTTPException(status_code=401, detail="Token has been revoked")

    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_type = payload.get("token_type")
        if token_type != TokenType.ACCESS:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
