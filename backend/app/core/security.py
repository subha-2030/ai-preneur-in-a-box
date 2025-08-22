import os
import secrets
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

from dotenv import load_dotenv
from jose import JWTError, jwt
from passlib.context import CryptContext

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token: str) -> Optional[str]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            return None
        return email
    except JWTError:
        return None


def create_oauth_state_token(user_id: str) -> str:
    """Create a JWT state token for OAuth flow with security features."""
    now = datetime.utcnow()
    expire = now + timedelta(minutes=10)  # 10-minute expiration
    nonce = secrets.token_urlsafe(32)  # Generate random nonce
    
    payload = {
        "user_id": user_id,
        "iat": now,
        "exp": expire,
        "nonce": nonce,
        "aud": "oauth_state"  # Audience for token purpose verification
    }
    
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_oauth_state_token(token: str) -> Optional[Dict[str, Any]]:
    """Decode and validate OAuth state token."""
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
            audience="oauth_state"  # Validate audience
        )
        
        # Verify required fields
        if not all(key in payload for key in ["user_id", "iat", "exp", "nonce", "aud"]):
            return None
            
        return payload
    except JWTError:
        return None
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    from app.db.repository import UserRepository
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    email = decode_token(token)
    if email is None:
        raise credentials_exception
    user_repo = UserRepository()
    user = await user_repo.get_user_by_email(email)
    if user is None:
        raise credentials_exception
    return user