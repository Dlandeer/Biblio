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
    ownship=session.exec(select(Book_Ownship,User).join(User)).all()
    return ownship

@router.delete("/ownship_history")
def purge_db(session: Session=Depends(get_session)):
    ownship=session.exec(select(Book_Ownship)).first()
    session.delete(ownship)
    session.commit()
    return {"message":"БД успешно отчищена"}

@router.get("/ownship_history/book/{book_id}")
def get_book_ownship_history( book_id: int,session: Session=Depends(get_session)):
    history = session.exec(select(Book_Ownship).where(Book_Ownship.book == book_id)).all()
    output = dict()
    if history is None or len(history)==0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"К сожалению, данной книги нет в нашей библиотеке или ее еще не брали"
            )
    else:
        for owner in history:
            user = session.exec(select(User).where(User.user_id==owner.owner)).first()
            output.update({owner.start_date + " - " + owner.end_date : user.name + ", email - " + user.email})
    return {"message":output}

@router.get("/ownship_history/user/{user_id}")
def get_user_history(user_id: int,session: Session=Depends(get_session)):
    user = session.exec(select(Book_Ownship).join(User).where(User.user_id==user_id)).all()
    output = dict()
    if user is None or len(user)==0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"К сожалению, пользователь с id {user_id} пока не брал книги или не существует"
            )
    else:
        for instance in user:
            book = session.exec(select(Book).where(Book.book_id==instance.book)).first()
            output.update({instance.start_date + " - " + instance.end_date : book.title + ", id - " + str(book.book_id)})
        return {"message" : output}