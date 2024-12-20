from contextlib import contextmanager

from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session

from db.models import Base

DATABASE_URL = "sqlite:///pinterest.db"


def create_db_engine():
    """Создание и возвращение объекта engine для подключения к базе данных."""
    engine = create_engine(DATABASE_URL, echo=False)  # Убрать echo=True в продакшене
    return engine


@contextmanager
def get_db(engine: Engine) -> Session:
    """Создание и возврат сессии для работы с базой данных."""
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    try:
        yield db  # Возвращаем сессию
    finally:
        db.close()


def create_tables(engine):
    Base.metadata.create_all(engine)


def delete_tables(engine):
    Base.metadata.drop_all(engine)
