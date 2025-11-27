"""
FILE: auth_middleware.py
PATH: yugnex/backend/api/middleware/auth_middleware.py
PURPOSE: Protects API routes by validating JWT tokens.
"""

from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from config.settings import settings
from database.connection import get_db
from database.models import User
from api.schemas.user import TokenData

# Standard scheme (Throws 401 if missing)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

# Optional scheme (Returns None if missing)
oauth2_scheme_optional = OAuth2PasswordBearer(tokenUrl="/api/auth/login", auto_error=False)

async def get_current_user(
    token: str = Depends(oauth2_scheme), 
    db: AsyncSession = Depends(get_db)
) -> User:
    """
    PURPOSE: Enforce authentication. Throws 401 if invalid.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
        
    result = await db.execute(select(User).where(User.username == token_data.username))
    user = result.scalar_one_or_none()
    
    if user is None:
        raise credentials_exception
        
    return user

async def get_current_user_optional(
    token: Optional[str] = Depends(oauth2_scheme_optional),
    db: AsyncSession = Depends(get_db)
) -> Optional[User]:
    """
    PURPOSE: Get user if logged in, otherwise return None. Does NOT throw 401.
    """
    if not token:
        return None
        
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return None
        token_data = TokenData(username=username)
    except JWTError:
        return None
        
    result = await db.execute(select(User).where(User.username == token_data.username))
    user = result.scalar_one_or_none()
    
    return user