import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

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

        self.configure(bg="#f7f7f7")

        tk.Label(
            self,
            text="Вход",
            font=("Arial", 20, "bold"),
            fg="#333333",
            bg="#f7f7f7",
        ).pack(pady=20)

        form_frame = tk.Frame(self, bg="#f7f7f7")
        form_frame.pack(pady=10)

        tk.Label(
            form_frame, text="Логин:", font=("Arial", 12), fg="#555555", bg="#f7f7f7"
        ).grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.login_entry = ttk.Entry(form_frame, font=("Arial", 12))
        self.login_entry.grid(row=0, column=1, padx=10, pady=5)
        self.login_entry.bind("<Return>", lambda _: self.password_entry.focus())

        tk.Label(
            form_frame, text="Пароль:", font=("Arial", 12), fg="#555555", bg="#f7f7f7"
        ).grid(row=1, column=0, padx=10, pady=5, sticky="w")

        self.password_entry = ttk.Entry(form_frame, font=("Arial", 12), show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=5)
        self.password_entry.bind("<Return>", lambda _: self.login())

        button_frame = tk.Frame(self, bg="#f7f7f7")
        button_frame.pack(pady=20)

        ttk.Button(button_frame, text="Войти", command=self.login).grid(
            row=0, column=0, padx=10
        )

        ttk.Button(
            button_frame, text="Регистрация", command=self.registration_window
        ).grid(row=0, column=1, padx=10)

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

        self.configure(bg="#f7f7f7")

        tk.Label(
            self,
            text="Регистрация",
            font=("Arial", 20, "bold"),
            fg="#333333",
            bg="#f7f7f7",
        ).pack(pady=20)

        form_frame = tk.Frame(self, bg="#f7f7f7")
        form_frame.pack(pady=10)

        tk.Label(
            form_frame, text="Логин:", font=("Arial", 12), fg="#555555", bg="#f7f7f7"
        ).grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.reg_login_entry = ttk.Entry(form_frame, font=("Arial", 12))
        self.reg_login_entry.grid(row=0, column=1, padx=10, pady=5)
        self.reg_login_entry.bind("<Return>", self.focus_next_field2)

        tk.Label(
            form_frame, text="Пароль:", font=("Arial", 12), fg="#555555", bg="#f7f7f7"
        ).grid(row=1, column=0, padx=10, pady=5, sticky="w")

        self.reg_password_entry = ttk.Entry(form_frame, font=("Arial", 12), show="*")
        self.reg_password_entry.grid(row=1, column=1, padx=10, pady=5)
        self.reg_password_entry.bind("<Return>", self.focus_next_field2)

        tk.Label(
            form_frame,
            text="Подтвердите пароль:",
            font=("Arial", 12),
            fg="#555555",
            bg="#f7f7f7",
        ).grid(row=2, column=0, padx=10, pady=5, sticky="w")

        self.reg_confirm_password_entry = ttk.Entry(
            form_frame, font=("Arial", 12), show="*"
        )
        self.reg_confirm_password_entry.grid(row=2, column=1, padx=10, pady=5)
        self.reg_confirm_password_entry.bind("<Return>", self.register_action)

        button_frame = tk.Frame(self, bg="#f7f7f7")
        button_frame.pack(pady=20)

        ttk.Button(
            button_frame, text="Зарегистрироваться", command=self.registration
        ).grid(row=0, column=0, padx=10)

        ttk.Button(button_frame, text="Назад", command=self.login_window).grid(
            row=0, column=1, padx=10
        )

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
