"""
Обращение к базе данных, функции для ее инициализации
"""

from sqlmodel import create_engine, Session,SQLModel
from app.config import settings as st
DB_URL = f"postgresql://{st.db_username}:{st.db_password}@{st.db_host}:{st.db_port}/{st.db_name}"
engine = create_engine(DB_URL, echo=True)

def get_session():
    """Получает сессию"""
    with Session(engine) as session:
        yield session

def init_database():
    """Инициализирует базу данных"""
    SQLModel.metadata.create_all(engine)
