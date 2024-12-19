import bcrypt
from sqlalchemy.orm import Session

from db.models import User
from utils import validate_password


class AuthCRUD:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_username(self, username: str):
        """Получить пользователя по имени"""
        return self.db.query(User).filter(User.username == username).first()

    def register_user(self, username: str, password: str):
        """Регистрация нового пользователя"""
        if self.get_user_by_username(username):
            return "Пользователь с данным именем уже существует."

        if not validate_password(password):
            return "Пароль должен содержать минимум 5 латинских букв и 3 цифры"

        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

        new_user = User(username=username, password=hashed_password.decode("utf-8"))
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)

        return "Регистрация успешна! Теперь можно войти."

    def login_user(self, username: str, password: str):
        """Авторизация пользователя"""
        user = self.get_user_by_username(username)

        if user is None:
            raise ValueError("Пользователь не найден.")

        if not bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
            raise ValueError("Неверный пароль.")

        return user
