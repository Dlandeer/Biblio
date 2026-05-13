from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session,select
from db import get_session
from scemas.bookC import User
from random import randint

router = APIRouter(prefix="/auth", tags=["Безопасность"])

@router.post("/sign_up", status_code=status.HTTP_201_CREATED)
def create_user(user:User, session:Session=Depends(get_session)):
    db_user=session.exec(select(User).where(User.email == user.email)).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Пользователь с почтой {user.email} уже существует"
)
    new_user=User(name=user.name, email=user.email, password=user.password)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user
            
@router.post("/login", status_code=status.HTTP_200_OK)
def login(login_attempt_data: OAuth2PasswordRequestForm = Depends(), db_session: Session = Depends(get_session)):
    statement = select(User).where(User.email == login_attempt_data.username)
    existing_user = db_session.exec(statement).first()
    print(existing_user)
    if not existing_user:
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Пользователь {login_attempt_data.username} не найден"
        )
    if existing_user.password == login_attempt_data.password:
        print(1)
        access_token = str(existing_user.user_id*112 - randint(10,30))
        print(access_token)
        return {
                "access_token": access_token,
                "token_type": "bearer"
                    }
    else:
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Неверный пароль для пользователя {login_attempt_data.username}"
        )