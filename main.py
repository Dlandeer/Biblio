from typing import List, Optional

from fastapi import FastAPI, HTTPException, status,Depends
from contextlib import asynccontextmanager

from scemas import bookC
from sqlmodel import Session, select
from sqlalchemy import text
from db import get_session, init_database

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_database()
    yield
app = FastAPI(lifespan=lifespan)


books: List[bookC.Book] = []
next_id = 1

@app.get("/test-db", status_code=status.HTTP_200_OK)
def test_database(session: Session = Depends(get_session)):
    result = session.exec(select(text("'Hello world'"))).all()
    return result

@app.post("/books",status_code=status.HTTP_201_CREATED)
def add_book(book: bookC.Book, session:Session=Depends(get_session)):
    global next_id
    global books
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

@app.get("/books/{book_id}",status_code=status.HTTP_200_OK, response_model=bookC.Book)
def get_book(book_id:int):
    global books
    for book in books:
        if book.id == book_id:
            return book
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Книга с id {book_id} не найдена")

@app.put("/books/{book_id}",status_code=status.HTTP_200_OK, response_model= bookC.BookResponse)
def upd_book(book_id:int, book:bookC.Book):
    global books
    for book1 in books:
        if book1.id == book_id:
            book.id=book_id
            books.remove(book1)
            books.append(book)
            return bookC.BookResponse(message = "Книга успешно обновлена", book=books[-1])
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Книга с id {book_id} не найдена")

@app.delete("/books/{book_id}",status_code=status.HTTP_200_OK, response_model= bookC.MessageResponse)
def del_book(book_id:int):
    global books
    global next_id
    for book in books:
        if book.id == book_id:
            books.remove(book)
            return bookC.MessageResponse(message="Книга удалена")
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Книга с id {book_id} не найдена")