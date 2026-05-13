from typing import List, Optional

from fastapi import FastAPI, HTTPException, status,Depends
from contextlib import asynccontextmanager

from scemas import bookC
from sqlmodel import Session, select
from sqlalchemy import text
from db import get_session, init_database
import auth

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_database()
    yield
app = FastAPI(lifespan=lifespan)

app.include_router(auth.router)

@app.get("/test-db", status_code=status.HTTP_200_OK)
def test_database(session: Session = Depends(get_session)):
    result = session.exec(select(bookC.User)).all()
    return result

@app.post("/books",status_code=status.HTTP_201_CREATED)
def add_book(book: bookC.Book, session:Session=Depends(get_session)):
    session.add(book)
    session.commit()
    session.refresh(book)
    return book

@app.get("/books",status_code=status.HTTP_200_OK)
def all_books(session: Session = Depends(get_session)):
    books = session.exec(select(bookC.Book)).all()
    if books is None or len(books) == 0:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail=f"К сожалению книг пока нет"
            )
    return books

@app.get("/books/{book_id}",status_code=status.HTTP_200_OK)
def get_book(book_id:int,session: Session = Depends(get_session)):
    book = session.exec(select(bookC.Book).where(bookC.Book.book_id == book_id)).all()
    if book is None or len(book) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"К сожалению, данной книги нет в нашей библиотеке"
            )
    return book[0]

@app.put("/books/{book_id}",status_code=status.HTTP_200_OK)
def upd_book(book_id:int, book:bookC.Book, session: Session = Depends(get_session)):
    up_book = session.exec(select(bookC.Book).where(bookC.Book.book_id == book_id)).first()
    if up_book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"К сожалению, данной книги нет в нашей библиотеке"
            )
    up_book.author=book.author
    up_book.year=book.year
    up_book.title=book.title
    session.add(up_book)
    session.commit()
    session.refresh(up_book)
    return up_book

@app.delete("/books/{book_id}",status_code=status.HTTP_200_OK, response_model= bookC.MessageResponse)
def del_book(book_id:int, session: Session = Depends(get_session)):
    del_book = session.exec(select(bookC.Book).where(bookC.Book.book_id == book_id)).first()
    if del_book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"К сожалению, данной книги нет в нашей библиотеке или она уже удалена из нее"
            )
    session.delete(del_book)
    session.commit()
    return {"message":"Книга успешно удалена"}