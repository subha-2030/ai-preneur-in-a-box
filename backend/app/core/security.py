import os
import secrets
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

from dotenv import load_dotenv
from jose import JWTError, jwt, ExpiredSignatureError
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.models.user import User

load_dotenv()

logger = logging.getLogger(__name__)
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


def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=7)
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
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
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

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    from app.db.repository import UserRepository
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        logger.debug(f"Decoding token: {token}")
        email = decode_token(token)
        if email is None:
            logger.warning("Token decoding failed or email is not in token.")
            raise credentials_exception
        
        logger.debug(f"Token decoded successfully. Email: {email}")
        user_repo = UserRepository()
        user = await user_repo.get_user_by_email(email)
        
        if user is None:
            logger.warning(f"User not found for email: {email}")
            raise credentials_exception
        
        logger.debug(f"User found: {user.email}")
        
        # If the user has Google Calendar credentials, check if they need to be refreshed
        if user.google_calendar_credentials:
            from google.oauth2.credentials import Credentials
            credentials = Credentials(**user.google_calendar_credentials)
            if credentials.expired and credentials.refresh_token:
                logger.info("Google Calendar credentials expired. Refreshing...")
                from google.auth.transport.requests import Request
                credentials.refresh(Request())
                user.google_calendar_credentials = {
                    'token': credentials.token,
                    'refresh_token': credentials.refresh_token,
                    'token_uri': credentials.token_uri,
                    'client_id': credentials.client_id,
                    'client_secret': credentials.client_secret,
                    'scopes': credentials.scopes
                }
                await user_repo.update_user(user)
                logger.info("Google Calendar credentials refreshed and updated in DB.")

        return user
    except HTTPException as e:
        logger.error(f"HTTPException in get_current_user: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"An unexpected error occurred in get_current_user: {e}")
        raise credentials_exception