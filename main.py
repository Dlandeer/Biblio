from typing import List, Optional

from fastapi import FastAPI, HTTPException, status

from scemas import bookC

app = FastAPI()


books: List[bookC.Book] = []
next_id = 1

@app.post("/books",status_code=status.HTTP_201_CREATED)
def add_book(book: bookC.Book):
    global next_id
    global books
    book.id=next_id
    next_id+=1
    books.append(book)
    return bookC.BookResponse(message = "Книга успешно добавлена", book = books[-1])

@app.get("/books",status_code=status.HTTP_200_OK, response_model=bookC.BooksResponse)
def all_books():
    global books
    return bookC.BooksResponse(books=books)

@app.get("/books/{book_id}",status_code=status.HTTP_200_OK, response_model=bookC.Book)
def get_book(book_id:int):
    global books
    for book in books:
        if book.id == book_id:
            return book
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Книга с id {book_id} не найдена")

@app.put("/books/{book_id}",status_code=status.HTTP_200_OK, response_model= bookC.BookResponse)
def upd_book(book_id:int, book:Book):
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