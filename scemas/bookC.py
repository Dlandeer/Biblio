from typing import List, Optional
from pydantic import BaseModel

class Book(BaseModel):
    id: Optional[int] = None
    title: str
    author: str
    year: int

class MessageResponse(BaseModel):
    message: str

class BookResponse(MessageResponse):
    book: Optional[Book] = None

class BooksResponse(BaseModel):
    books: List[Book]