from typing import Annotated
from fastapi import APIRouter, status, Depends, HTTPException
from db import get_session
from fastapi.security import OAuth2PasswordBearer
from auth import get_current_user
from scemas.bookC import User,Book,Book_Ownship
from sqlmodel import Session, select
from datetime import timedelta,timezone,datetime

router=APIRouter(prefix="/book_ownship")

@router.post("/add")
def get_book(book_name:str, user: Annotated[User, Depends(get_current_user)], session: Session=Depends(get_session)):
    books=session.exec(select(Book).where(Book.title==book_name)).all()
    if books is None or len(books)==0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f"К сожалению, данной книги нет в нашей библиотеке")
    for i in range(len(books)):
        ownship=session.exec(select(Book_Ownship).join(Book).where(Book.book_id == books[i].book_id)).first()
        if ownship is None:
            new_ownship=Book_Ownship(owner=user.user_id,book=books[i].book_id,start_date=str(datetime.now().date()),end_date=str(datetime.now().date()+timedelta(days=14)))
            session.add(new_ownship)
            session.commit()
            session.refresh(new_ownship)
            return new_ownship
        else:
            if datetime.strptime(ownship.end_date, '%Y-%m-%d') < datetime.today():
                new_ownship=Book_Ownship(owner=user.user_id,book=books[i].book_id,start_date=str(datetime.now().date()),end_date=str(datetime.now().date()+timedelta(days=14)))
                session.add(new_ownship)
                session.commit()
                session.refresh(new_ownship)
                return new_ownship
            elif datetime.strptime(ownship.end_date, '%Y-%m-%d') == datetime.today() and user.user_id == ownship.owner:
                new_ownship=Book_Ownship(owner=user.user_id,book=books[i].book_id,start_date=str(datetime.now().date()),end_date=str(datetime.now().date()+timedelta(days=14)))
                session.add(new_ownship)
                session.commit()
                session.refresh(new_ownship)
                return new_ownship
            else:
                if i == len(books)-1:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f"К сожалению, данная книга уже взята")
                else:
                    continue
            

@router.get("/ownship_history")
def get_ownship_history(session: Session=Depends(get_session)):
    ownship=session.exec(select(Book_Ownship)).all()
    return ownship

@router.delete("/ownship_history")
def purge_db(session: Session=Depends(get_session)):
    ownship=session.exec(select(Book_Ownship)).first()
    session.delete(ownship)
    session.commit()
    return {"message":"БД успешно отчищена"}