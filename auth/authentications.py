import logging

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from typing import Optional
from datetime import datetime, timedelta
from models.db import get_db
from models.models import User
from sqlalchemy.orm import Session

# Define OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")



# JWT token related constants
SECRET_KEY = "secret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Password hashing utility
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

logger = logging.getLogger(__name__)

# Verify password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Hash password
def get_password_hash(password):
    return pwd_context.hash(password)

# Authenticate user
def authenticate_user(username: str, password: str,db: Session):
    
    user = db.query(User).filter(User.email == username).first()
    if not user or not verify_password(password, user.password):
        return False
    return user

# Create access token
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Dependency to get current user based on token
async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return None
    except JWTError:
        logger.error(f"get_current_user  {JWTError}")
        return None
    user = db.query(User).filter(User.name == username).first()
    if user is None:
        return None
    return user