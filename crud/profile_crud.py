import bcrypt
from sqlalchemy.orm import Session

from db.models import User
from utils import validate_password


class UserCRUD:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_username(
        self,
        username: str,
    ):
        return self.db.query(User).filter(User.username == username).first()

    def update_user(
        self, username: str, new_username: str = None, password: str = None
    ):
        user = self.get_user_by_username(username)
        if user is None:
            raise ValueError("Пользователь не найден.")

        if new_username and new_username != user.username:
            if self.get_user_by_username(new_username):
                raise ValueError("Пользователь с таким именем уже существует.")
            user.username = new_username

        if password:
            check_password = validate_password(password)
            if not check_password:
                raise ValueError(
                    "Пароль должен содержать минимум 5 латинских букв и 3 цифры"
                )
            user.password = bcrypt.hashpw(
                password.encode("utf-8"), bcrypt.gensalt()
            ).decode("utf-8")

        self.db.commit()
        self.db.refresh(user)
        return user
