import tkinter as tk
from sqlalchemy.orm import Session

from crud.user_crud import UserCRUD
from crud.posts_crud import (
    PostsCRUD,
)
from interface.auth_screen import AuthInterface
from interface.main_screen import MainInterface


class InterfaceManager:
    def __init__(self, master, db: Session):
        self.user_crud = UserCRUD(db)
        self.posts_crud = PostsCRUD(db)  # Вот здесь мы создаем экземпляр постов CRUD
        self.master = master
        self.current_interface = None
        self.current_user = None

    def show_interface(self, interface_class, user=None, *args, **kwargs):
        if self.current_interface:
            self.current_interface.destroy()

        # Если пользователь не передан, берём текущего
        user = user or self.current_user

        self.current_interface = interface_class(
            self.master, self, user, self.main_window, *args, **kwargs
        )
        self.current_interface.pack(fill=tk.BOTH, expand=True)

    def login_success(self, user):
        self.current_user = user
        self.show_interface(MainInterface, user=user)

    def logout_success(self):
        self.current_user = None
        self.show_interface(AuthInterface)

    def main_window(self):
        self.show_interface(MainInterface, user=self.current_user)

    def show_profile_interface(self, user):
        from interface.profile_screen import ProfileInterface

        self.show_interface(ProfileInterface, user=user)
