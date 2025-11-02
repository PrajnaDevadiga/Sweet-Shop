from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from .database import get_db
from .models import User
from .schemas import TokenData

SECRET_KEY = "your-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Configure passlib to handle bcrypt without version checking issues
# Suppress the version check error by using a try-except during initialization
try:
    pwd_context = CryptContext(
        schemes=["bcrypt"],
        deprecated="auto",
    )
except (AttributeError, TypeError):
    # Fallback if there are version compatibility issues
    pwd_context = CryptContext(schemes=["bcrypt"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")


def _truncate_password(password: str) -> str:
    """
    Truncate password to 72 bytes (bcrypt limit).
    Passwords longer than 72 bytes will be truncated character by character
    to avoid cutting multi-byte UTF-8 characters in the middle.
    """
    password_bytes = password.encode('utf-8')
    if len(password_bytes) <= 72:
        return password
    
    # Truncate character by character until under 72 bytes
    truncated = password
    while len(truncated.encode('utf-8')) > 72:
        truncated = truncated[:-1]
    
    return truncated


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    try:
        # Truncate to 72 bytes to match how it was hashed
        password_bytes = plain_password.encode('utf-8')
        if len(password_bytes) > 72:
            password_bytes = password_bytes[:72]
            plain_password = password_bytes.decode('utf-8', errors='ignore')
        
        return pwd_context.verify(plain_password, hashed_password)
    except (ValueError, AttributeError) as e:
        # Handle bcrypt errors gracefully
        if "longer than 72 bytes" in str(e):
            # Try with shorter password
            safe_password = plain_password.encode('utf-8')[:70].decode('utf-8', errors='ignore')
            return pwd_context.verify(safe_password, hashed_password)
        return False


def get_password_hash(password: str) -> str:
    """
    Hash a password.
    Passwords longer than 72 bytes will be truncated automatically.
    """
    # Truncate to 72 bytes (bcrypt limit) - do it as bytes to be safe
    password_bytes = password.encode('utf-8')
    if len(password_bytes) > 72:
        # Truncate to exactly 72 bytes
        password_bytes = password_bytes[:72]
        # Decode back, using 'ignore' to handle any partial UTF-8 characters
        password = password_bytes.decode('utf-8', errors='ignore')
    
    try:
        return pwd_context.hash(password)
    except ValueError as e:
        # If still fails, try with even shorter password
        if "longer than 72 bytes" in str(e):
            # Force truncate to 70 bytes as safety margin
            safe_password = password.encode('utf-8')[:70].decode('utf-8', errors='ignore')
            return pwd_context.hash(safe_password)
        raise


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_user_by_username(db: Session, username: str) -> Optional[User]:
    """Get user by username"""
    return db.query(User).filter(User.username == username).first()


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Get user by email"""
    return db.query(User).filter(User.email == email).first()


def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    """Authenticate a user"""
    user = get_user_by_username(db, username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> User:
    """Get current authenticated user from JWT token"""
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
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_admin_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """Get current authenticated admin user"""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return current_user

