"""
Взаимодействие пользователей и книг, возможности взять и вернуть книгу
Доступ к истории владения книгами
"""

from datetime import timedelta,datetime
from typing import Annotated
from sqlmodel import Session, select
from fastapi import APIRouter, status, Depends, HTTPException
from app.db import get_session
from app.auth import get_current_user
from app.scemas.models import User,Book,BookOwnship

router=APIRouter(prefix="/book_ownship", tags=["Выдача книг"])

@router.post("/add")
def get_book(book_name:str, user: Annotated[User, Depends(get_current_user)],
            session: Session=Depends(get_session)):
    """Выдача книги пользователю по названию книги"""
    books=session.exec(select(Book).where(Book.title==book_name)).all()
    if books is None or len(books)==0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail="К сожалению, данной книги нет в нашей библиотеке")
    for book in books:
        statement = select(BookOwnship).join(Book).where(Book.book_id == book.book_id)
        ownship=session.exec(statement).first()
        if ownship is None:
            new_ownship=BookOwnship(owner=user.user_id,book=book.book_id,
                                     start_date=str(datetime.now().date()),
                                     end_date=str(datetime.now().date()+timedelta(days=14)))
            session.add(new_ownship)
            session.commit()
            session.refresh(new_ownship)
            return new_ownship
        if datetime.strptime(ownship.end_date, '%Y-%m-%d') <= datetime.today():
            new_ownship=BookOwnship(owner=user.user_id,book=book.book_id,
                                         start_date=str(datetime.now().date()),
                                         end_date=str(datetime.now().date()+timedelta(days=14)))
            session.add(new_ownship)
            session.commit()
            session.refresh(new_ownship)
            return new_ownship
        continue
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail="К сожалению, данная книга уже взята")

@router.put("/return")
def return_book(book_name:str, user: Annotated[User, Depends(get_current_user)],
            session: Session=Depends(get_session)):
    """Досрочно возвращает книгу"""
    book=session.exec(select(BookOwnship).join(Book).where(Book.title==book_name)).first()
    if book is None or book.owner != user.user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail="К сожалению, данная книга взята не вами")
    if book.end_date == str(datetime.now().date()):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail="Книга уже возвращена")
    book.end_date = str(datetime.now().date())
    session.add(book)
    session.commit()
    session.refresh(book)
    return book

@router.get("/ownship_history")
def get_ownship_history(session: Session=Depends(get_session)):
    """Получает полную историю владения, сгруппированную по пользователю"""
    users = session.exec(select(User)).all()
    if users is None or len(users)==0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="К сожалению, книги пока не брали"
            )
    output = {}
    for user in users:
        output1={}
        books=session.exec(select(BookOwnship).where(BookOwnship.owner==user.user_id)).all()
        if books is None or len(books)==0:
            output.update({user.email : "Не брал книг"})
            continue
        for book in books:
            book_instance=session.exec(select(Book).where(Book.book_id==book.book)).first()
            output1.update({book.start_date + " - " + book.end_date :
                             book_instance.title + ", id - " + str(book.book)})
        output.update({user.email : output1})
    return {"message":output}

@router.get("/ownship_history/book/{book_id}")
def get_book_ownship_history( book_id: int,session: Session=Depends(get_session)):
    """Получает историю владения книгой по ее id"""
    history = session.exec(select(BookOwnship).where(BookOwnship.book == book_id)).all()
    output = {}
    if history is None or len(history)==0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="К сожалению, данной книги нет в нашей библиотеке или ее еще не брали"
            )
    for owner in history:
        user = session.exec(select(User).where(User.user_id==owner.owner)).first()
        output.update({owner.start_date + " - " + owner.end_date :
                            user.name + ", email - " + user.email})
    return {"message":output}

@router.get("/ownship_history/user/{user_id}")
def get_user_history(user_id: int,session: Session=Depends(get_session)):
    """Получает историю взятых пользователем книг по его id"""
    user = session.exec(select(BookOwnship).join(User).where(User.user_id==user_id)).all()
    output = {}
    if user is None or len(user)==0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"К сожалению, пользователь с id {user_id} пока не брал книги или не существует"
            )
    for instance in user:
        book = session.exec(select(Book).where(Book.book_id==instance.book)).first()
        output.update({instance.start_date + " - " + instance.end_date :
                            book.title + ", id - " + str(book.book_id)})
    return {"message" : output}
