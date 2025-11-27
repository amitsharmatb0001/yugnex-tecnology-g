"""
FILE: auth.py
PATH: yugnex/backend/api/routes/auth.py
PURPOSE: Handles User Registration, Login, and Token generation.
WORKING:
    1. /register: Hashes password, saves user to DB.
    2. /login: Verifies password, returns JWT access token.
    3. /me: Returns current user details using auth middleware.
USAGE:
    POST /api/auth/register -> {email, username, password}
    POST /api/auth/login -> {username, password} (Form Data)
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from datetime import timedelta

from database.connection import get_db
from database.models import User
from services.auth_service import AuthService
from api.schemas.user import UserCreate, UserResponse, Token
from api.middleware.auth_middleware import get_current_user
from config.settings import settings

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserResponse)
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    """
    PURPOSE: Register a new user.
    FLOW: Check duplicates -> Hash Password -> Save to DB.
    """
    
    # Check if user exists (email or username)
    query = select(User).where(
        or_(User.email == user_in.email, User.username == user_in.username)
    )
    result = await db.execute(query)
    existing_user = result.scalar_one_or_none()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or Email already registered"
        )
    
    # Create new user
    hashed_password = AuthService.get_password_hash(user_in.password)
    new_user = User(
        email=user_in.email,
        username=user_in.username,
        full_name=user_in.full_name,
        password_hash=hashed_password,
        role="user"
    )
    
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    
    return new_user

@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: AsyncSession = Depends(get_db)
):
    """
    PURPOSE: Authenticate user and return JWT.
    NOTE: OAuth2PasswordRequestForm requires 'username' and 'password' fields.
    """
    
    # Find user
    result = await db.execute(select(User).where(User.username == form_data.username))
    user = result.scalar_one_or_none()
    
    # Verify password
    if not user or not AuthService.verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = AuthService.create_access_token(
        data={"sub": user.username, "role": user.role},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_user)):
    """
    PURPOSE: Get details of the currently logged-in user.
    PARAMS: Uses Auth Middleware to decode token.
    """
    return current_user