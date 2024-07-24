import os
from datetime import datetime, timedelta
from jose import jwt
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict) -> str:
    try:
        secret = os.getenv('JWT_SECRET_KEY')
        algorithm = os.getenv('JWT_ALGORITHM')
        expire_minutes = int(os.getenv('JWT_EXPIRE_MINUTES', 120))
    except KeyError:
        raise Exception("JWT configuration not found")
    time_now = datetime.now(datetime.UTC)
    expire_time = time_now + timedelta(minutes=expire_minutes)
    payload = data.copy()
    payload.update({
        "exp": expire_time,
        "iat": time_now,
    })
    encoded_jwt = jwt.encode(payload, secret, algorithm=algorithm)
    return encoded_jwt

def decode_access_token(token: str) -> dict:
    try:
        secret = os.getenv('JWT_SECRET_KEY')
        algorithm = os.getenv('JWT_ALGORITHM')
    except KeyError:
        raise Exception("JWT configuration not found")
    return jwt.decode(token, secret, algorithms=[algorithm])
