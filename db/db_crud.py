import bcrypt
from sqlalchemy.orm import Session

from db.base import get_db
from db.models import User
from utils import validate_password


def get_user_by_nickname(
    db: Session,
    username: str,
):
    return db.query(User).filter(User.username == username).first()


def register_user(
    db: Session,
    username: str,
    password: str,
):
    if get_user_by_nickname(db, username):
        return f"Пользователь с данным именем уже существует."

    check_password = validate_password(password)

    if not check_password:
        return f"Пароль должен содержать минимум 5 латинских букв и 3 цифры"

    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    new_user = User(username=username, password=hashed_password.decode("utf-8"))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
