"""
FILE: auth_service.py
PATH: yugnex/backend/services/auth_service.py
PURPOSE: Handles core authentication logic (hashing, JWT).
WORKING:
    1. Uses bcrypt directly for password hashing (compatible with bcrypt 4.x+).
    2. Provides methods to verify and hash passwords.
    3. Generates JWT tokens with expiration using python-jose.
USAGE:
    hash = AuthService.get_password_hash("secret")
    token = AuthService.create_access_token({"sub": "user"})
"""

from datetime import datetime, timedelta
from typing import Optional
import bcrypt
from jose import JWTError, jwt
from config.settings import settings

# Password Hashing Configuration
# Using bcrypt directly for better compatibility with bcrypt 4.x
BCRYPT_ROUNDS = 12

class AuthService:
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        PURPOSE: Verify if a plain password matches the hash.
        PARAMS: plain_password, hashed_password
        RETURNS: bool (True if match)
        """
        try:
            # Convert strings to bytes if needed
            password_bytes = plain_password.encode('utf-8')
            hash_bytes = hashed_password.encode('utf-8') if isinstance(hashed_password, str) else hashed_password
            
            # Truncate password to 72 bytes (bcrypt limit)
            if len(password_bytes) > 72:
                password_bytes = password_bytes[:72]
            
            return bcrypt.checkpw(password_bytes, hash_bytes)
        except Exception:
            return False

    @staticmethod
    def get_password_hash(password: str) -> str:
        """
        PURPOSE: Generate a secure hash for a password.
        PARAMS: password (plain text)
        RETURNS: str (hashed string)
        NOTE: bcrypt has a 72-byte limit, so we truncate if necessary
        """
        # Convert to bytes and truncate to 72 bytes if needed
        password_bytes = password.encode('utf-8')
        if len(password_bytes) > 72:
            password_bytes = password_bytes[:72]
        
        # Generate salt and hash
        salt = bcrypt.gensalt(rounds=BCRYPT_ROUNDS)
        hashed = bcrypt.hashpw(password_bytes, salt)
        
        # Return as string
        return hashed.decode('utf-8')

    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """
        PURPOSE: Generate a JWT access token.
        PARAMS: data (dict of claims), expires_delta (optional duration)
        RETURNS: str (encoded JWT)
        """
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
            
        to_encode.update({"exp": expire})
        
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt