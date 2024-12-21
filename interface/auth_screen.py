import tkinter as tk
from tkinter import messagebox

from db.base import get_db, create_db_engine
from crud.auth_crud import AuthCRUD


class AuthInterface(tk.Frame):
    def __init__(self, master, manager, main_window, user=None):
        super().__init__(master)
        self.manager = manager

        # Инициализация AuthCRUD
        engine = create_db_engine()
        with get_db(engine) as db_session:
            self.auth_crud = AuthCRUD(db_session)

        # Элементы интерфейса
        self.login_entry = None
        self.password_entry = None
        self.reg_login_entry = None
        self.reg_password_entry = None
        self.reg_confirm_password_entry = None

        self.username = None
        self.search_entry = None

        self.login_window()

    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()

    def login_window(self):
        self.clear_window()
        tk.Label(
            self,
            text="Вход",
            font=("Arial", 18, "bold"),
            fg="#4B0082",
            bg="#F0F0F0",
        ).pack(pady=20)

        tk.Label(
            self, text="Логин:", font=("Arial", 12), fg="#4B0082", bg="#F0F0F0"
        ).pack()
        self.login_entry = tk.Entry(
            self, font=("Arial", 12), bg="white", fg="black", bd=2, relief="solid"
        )
        self.login_entry.pack(pady=5)
        self.login_entry.bind(
            "<Return>", lambda _: self.password_entry.focus()
        )  # Фокус на пароль

        tk.Label(
            self, text="Пароль:", font=("Arial", 12), fg="#4B0082", bg="#F0F0F0"
        ).pack()
        self.password_entry = tk.Entry(
            self,
            font=("Arial", 12),
            bg="white",
            fg="black",
            bd=2,
            relief="solid",
            show="*",
        )
        self.password_entry.pack(pady=5)
        self.password_entry.bind("<Return>", lambda _: self.login())  # Вход при Enter

        tk.Button(
            self,
            text="Войти",
            font=("Arial", 12),
            bg="#4B0082",
            fg="white",
            relief="solid",
            command=self.login,
        ).pack(pady=10)
        tk.Button(
            self,
            text="Регистрация",
            font=("Arial", 12),
            bg="#8A2BE2",
            fg="white",
            relief="solid",
            command=self.registration_window,
        ).pack(pady=5)

    def login(self):
        username = self.login_entry.get()
        password = self.password_entry.get()

        try:
            user = self.auth_crud.login_user(username, password)
            messagebox.showinfo("Успех", f"Добро пожаловать, {username}!")
            self.manager.login_success(user=user)
        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))

    def registration_window(self):
        self.clear_window()

        tk.Label(
            self,
            text="Регистрация",
            font=("Arial", 18, "bold"),
            fg="#4B0082",
            bg="#F0F0F0",
        ).pack(pady=20)

        tk.Label(
            self, text="Логин:", font=("Arial", 12), fg="#4B0082", bg="#F0F0F0"
        ).pack()
        self.reg_login_entry = tk.Entry(
            self, font=("Arial", 12), bg="white", fg="black", bd=2, relief="solid"
        )
        self.reg_login_entry.pack(pady=5)
        self.reg_login_entry.bind("<Return>", self.focus_next_field2)

        tk.Label(
            self, text="Пароль:", font=("Arial", 12), fg="#4B0082", bg="#F0F0F0"
        ).pack()
        self.reg_password_entry = tk.Entry(
            self,
            font=("Arial", 12),
            bg="white",
            fg="black",
            bd=2,
            relief="solid",
            show="*",
        )
        self.reg_password_entry.pack(pady=5)
        self.reg_password_entry.bind("<Return>", self.focus_next_field2)

        tk.Label(
            self,
            text="Подтвердите пароль:",
            font=("Arial", 12),
            fg="#4B0082",
            bg="#F0F0F0",
        ).pack()
        self.reg_confirm_password_entry = tk.Entry(
            self,
            font=("Arial", 12),
            bg="white",
            fg="black",
            bd=2,
            relief="solid",
            show="*",
        )
        self.reg_confirm_password_entry.pack(pady=5)
        self.reg_confirm_password_entry.bind("<Return>", self.register_action)

        tk.Button(
            self,
            text="Зарегистрироваться",
            font=("Arial", 12),
            bg="#4B0082",
            fg="white",
            relief="solid",
            command=self.registration,
        ).pack(pady=10)
        tk.Button(
            self,
            text="Назад",
            font=("Arial", 12),
            bg="#8A2BE2",
            fg="white",
            relief="solid",
            command=self.login_window,
        ).pack(pady=5)

    def focus_next_field2(self, event=None):
        widget = event.widget
        if widget == self.reg_login_entry:
            self.reg_password_entry.focus()
        elif widget == self.reg_password_entry:
            self.reg_confirm_password_entry.focus()
        elif widget == self.reg_confirm_password_entry:
            self.registration()

    def registration(self):
        username = self.reg_login_entry.get()
        password = self.reg_password_entry.get()
        confirm_password = self.reg_confirm_password_entry.get()

        if password != confirm_password:
            messagebox.showerror(
                "Ошибка", "Пароли не совпадают. Пожалуйста, введите пароли заново."
            )
            return

        message = self.auth_crud.register_user(username, password)

        if message == "Регистрация успешна! Теперь можно войти.":
            messagebox.showinfo("Успех", message)
            self.login_window()
        else:
            messagebox.showerror("Ошибка", message)

    def register_action(self, event=None):
        self.registration()
