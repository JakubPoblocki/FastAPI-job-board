from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, HTTPAuthorizationCredentials

from datetime import timedelta

from jose import jwt, JWTError

from app.config import SECRET_KEY, ALGORITHM
from app.crud import authenticate_user
from app.dependencies import get_db, bearer_scheme
from app.models import User, TokenBlacklist
from app.utils import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, TokenType, is_token_blacklisted
from sqlalchemy.orm import Session

router = APIRouter()


# ---------------- AUTH ROUTE ----------------
@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Endpoint to obtain an access token using username and password.
    Raises HTTPException if the credentials are invalid.

    :param form_data:
    :param db:
    :return:
    """
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": TokenType.ACCESS}


@router.post("/logout")
def logout_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
                db: Session = Depends(get_db)):
    """Endpoint to log out the user by blacklisting the provided token.

    :param credentials:
    :param db:
    :return: Success message.
    """
    token = credentials.credentials
    db.add(TokenBlacklist(token=token))
    db.commit()
    return {"msg": "Logged out successfully"}


@router.post("/refresh_token")
async def refresh_access_token(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db)
):
    """Endpoint to refresh the access token using a valid refresh token.
    Raises HTTPException if the refresh token is invalid or revoked.

    :param credentials:
    :param db:
    :return: New access token and the same refresh token.
    """
    refresh_token = credentials.credentials

    # Check if the refresh token is blocked
    if is_token_blacklisted(refresh_token, db):
        raise HTTPException(status_code=401, detail="Refresh token has been revoked")

    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        token_type = payload.get("token_type")
        if username is None or token_type != TokenType.REFRESH:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    user = db.query(User).filter(User.username == username).first()
    if user is None or user.disabled:
        raise HTTPException(status_code=401, detail="User not found or inactive")

    # Create a new access token
    access_token = create_access_token({"sub": user.username})

    return {"access_token": access_token, "refresh_token": refresh_token}