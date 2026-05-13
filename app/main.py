from fastapi import FastAPI
from contextlib import asynccontextmanager
from db import init_database
import auth,connections,book_handling

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_database()
    yield
app = FastAPI(lifespan=lifespan)

app.include_router(auth.router)
app.include_router(connections.router)
app.include_router(book_handling.router)