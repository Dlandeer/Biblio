from typing import List, Optional
from pydantic import BaseModel,EmailStr
from sqlmodel import SQLModel, Field as SQLField
from datetime import datetime

class Book(SQLModel, table=True):
    book_id: int = SQLField(default=None, nullable=False, primary_key=True)
    title: str
    author: str
    year: int

class User(SQLModel, table=True):
    user_id: int = SQLField(default=None, nullable=False, primary_key=True)
    email: EmailStr = SQLField(nullable=True, unique_items=True)
    password: str | None
    name: str
    class Config:
        json_schema_extra = {
        "example": {
        "name": "Иван Иванов",
        "email": "user@example.com",
        "password": "qwerty"
            }
        }

class Book_Ownship(SQLModel, table=True):
    operation_id: int = SQLField(default=None, nullable=False, primary_key=True)
    book: int = SQLField(foreign_key="Book.book_id")
    owner: int = SQLField(foreign_key="User.user_id")
    start_date: datetime.date
    end_date: datetime.date

class MessageResponse(BaseModel):
    message: str

class BookResponse(MessageResponse):
    book: Optional[Book] = None

class BooksResponse(BaseModel):
    books: List[Book]