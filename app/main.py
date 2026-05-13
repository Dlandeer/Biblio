"""
Основной файл приложения, соединяет все функции, отвечает за инициализацию базы данных
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.db import init_database
from app import auth,connections,book_handling

@asynccontextmanager
async def lifespan(fastapp: FastAPI):
    """Инициализирует базу данных"""
    init_database()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(auth.router)
app.include_router(connections.router)
app.include_router(book_handling.router)
