from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
import os
from app.db.db import get_db
from app.models.user import User
import logging

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/users/token")

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "test-secret-key-for-development")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

def get_current_user(
    request: Request,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    logging.warning(f"Session content: {dict(request.session) if hasattr(request, 'session') else 'No session'}")
    logging.warning(f"Authorization token: {token}")
    username = request.session.get("username") if hasattr(request, 'session') else None
    if username:
        user = db.query(User).filter(User.username == username).first()
        if user:
            logging.warning(f"Authenticated via session as user: {username}")
            return user
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    logging.warning(f"Authenticated via JWT as user: {username}")
    return user
