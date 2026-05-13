from typing import Annotated
from fastapi import APIRouter, status, Depends, HTTPException
from db import get_session
from fastapi.security import OAuth2PasswordBearer
from auth import get_current_user
from scemas.bookC import User,Book,Book_Ownship
from sqlmodel import Session

router=APIRouter(prefix="/book_ownship")

@router.post("/add")
def get_book(book_name:str, user: Annotated[User, Depends(get_current_user)], session: Session=Depends(get_session)):
    books=session.exec()