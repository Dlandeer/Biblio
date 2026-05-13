from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db import init_database
import app.auth as auth,app.connections as connections,app.book_handling as book_handling

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_database()
    yield
app = FastAPI(lifespan=lifespan)

app.include_router(auth.router)
app.include_router(connections.router)
app.include_router(book_handling.router)