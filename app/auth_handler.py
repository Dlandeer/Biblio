"""
Вспомогательный файл для модуля авторизации
"""

from datetime import timedelta,timezone,datetime
from jose import JWTError, jwt
from fastapi import HTTPException,status,Depends
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session,select
from passlib.context import CryptContext
from app.db import get_session
from app.scemas.models import User
from app.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """Создает токен доступа"""
    to_encode=data.copy()
    if expires_delta:
        expire=datetime.now(timezone.utc) + expires_delta
    else:
        expire=(datetime.now(timezone.utc) + timedelta(minutes=15))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algo)
    return encoded_jwt

def get_current_user(session:Session = Depends(get_session),token: str = Depends(oauth2_scheme)):
    """Получает текущего пользователя из токена доступа"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Пользователь не авторизован",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=settings.algo)
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError as exc:
        raise credentials_exception from exc

    user = session.exec(select(User).where(User.email==email)).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден"
        )
    return user

def get_password_hash(password):
    """Создает хэш пароля"""
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    """Проверяет пароль"""
    return pwd_context.verify(plain_password, hashed_password)
