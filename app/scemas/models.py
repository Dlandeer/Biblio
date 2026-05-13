"""
Основные классы необходимые для работы проекта
"""

from pydantic import BaseModel,EmailStr
from sqlmodel import SQLModel, Field as SQLField,UniqueConstraint

class Book(SQLModel, table=True):
    """Таблица книг"""
    book_id: int = SQLField(default=None, nullable=False, primary_key=True)
    title: str
    author: str
    year: int
    class Config:
        """Форма для добавления книги"""
        json_schema_extra = {
        "example": {
        "title": "История господина Н",
        "author": "Некто Нектонович",
        "year": 2001
            }
        }

class User(SQLModel, BaseModel, table=True):
    """Таблица пользователей"""
    __table_args__ = (UniqueConstraint("email"),)
    user_id: int = SQLField(default=None, nullable=False, primary_key=True)
    email: EmailStr = SQLField(nullable=True, unique_items=True)
    password: str | None
    name: str
    class Config:
        """Форма для добавления пользователей"""
        json_schema_extra = {
        "example": {
        "name": "Иван Иванов",
        "email": "user@example.com",
        "password": "qwerty"
            }
        }

class BookOwnship(SQLModel, table=True):
    """Таблица владения книгами"""
    operation_id: int = SQLField(default=None, nullable=False, primary_key=True)
    book: int = SQLField(foreign_key="book.book_id")
    owner: int = SQLField(foreign_key="user.user_id")
    start_date: str
    end_date: str
