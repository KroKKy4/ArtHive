import sqlite3

from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session

DATABASE_URL = "sqlite:///pinterest.db"


def create_db_engine():
    """Создание и возвращение объекта engine для подключения к базе данных."""
    engine = create_engine(DATABASE_URL, echo=False)  # Убрать echo=True в продакшене
    return engine


def get_db(engine: Engine) -> Session:
    """Создание и возврат сессии для работы с базой данных."""
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    try:
        yield db  # Возвращаем сессию
    finally:
        db.close()
