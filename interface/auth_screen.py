import tkinter as tk
from tkinter import messagebox

from db.base import get_db, create_db_engine
from db.db_crud import login_user, register_user


class Interface:
    def __init__(self, root):
        self.root = root
        self.root.title("ArtHive")
        self.root.geometry("400x360")
        self.root.config(bg="#FFFFFF")

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
        for widget in self.root.winfo_children():
            widget.destroy()

    def login_window(self):
        self.clear_window()
        tk.Label(
            self.root,
            text="Вход",
            font=("Arial", 18, "bold"),
            fg="#4B0082",
            bg="#FFFFFF",
        ).pack(pady=20)

        tk.Label(
            self.root, text="Логин:", font=("Arial", 12), fg="#4B0082", bg="#FFFFFF"
        ).pack()
        self.login_entry = tk.Entry(
            self.root, font=("Arial", 12), bg="white", fg="black", bd=2, relief="solid"
        )
        self.login_entry.pack(pady=5)

        tk.Label(
            self.root, text="Пароль:", font=("Arial", 12), fg="#4B0082", bg="#FFFFFF"
        ).pack()
        self.password_entry = tk.Entry(
            self.root,
            font=("Arial", 12),
            bg="white",
            fg="black",
            bd=2,
            relief="solid",
            show="*",
        )
        self.password_entry.pack(pady=5)

        tk.Button(
            self.root,
            text="Войти",
            font=("Arial", 12),
            bg="#4B0082",
            fg="white",
            relief="solid",
            command=self.login,
        ).pack(pady=10)
        tk.Button(
            self.root,
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

        engine = create_db_engine()
        with get_db(engine) as db:
            try:
                user = login_user(db, username, password)
                messagebox.showinfo("Успех", f"Добро пожаловать, {user.username}!")
                self.username = user.username
                self.main_window()
            except ValueError as e:
                messagebox.showerror("Ошибка", str(e))
            finally:
                db.close()

    def main_window(self):
        self.clear_window()
        self.root.geometry("900x500")

        top_frame = tk.Frame(self.root, bg="#FFFFFF")
        top_frame.pack(fill="x", pady=10)

        search_label = tk.Label(
            top_frame,
            text="Поиск изображений:",
            font=("Arial", 12),
            fg="#4B0082",
            bg="#FFFFFF",
        )
        search_label.pack(side="left", padx=10)

        self.search_entry = tk.Entry(
            top_frame, font=("Arial", 12), bg="white", fg="black", bd=2, relief="solid"
        )
        self.search_entry.pack(side="left", padx=10, pady=5)

    def registration_window(self):
        self.clear_window()

        tk.Label(
            self.root,
            text="Регистрация",
            font=("Arial", 18, "bold"),
            fg="#4B0082",
            bg="#FFFFFF",
        ).pack(pady=20)

        tk.Label(
            self.root, text="Логин:", font=("Arial", 12), fg="#4B0082", bg="#FFFFFF"
        ).pack()
        self.reg_login_entry = tk.Entry(
            self.root, font=("Arial", 12), bg="white", fg="black", bd=2, relief="solid"
        )
        self.reg_login_entry.pack(pady=5)
        self.reg_login_entry.bind("<Return>", self.focus_next_field2)

        tk.Label(
            self.root, text="Пароль:", font=("Arial", 12), fg="#4B0082", bg="#FFFFFF"
        ).pack()
        self.reg_password_entry = tk.Entry(
            self.root,
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
            self.root,
            text="Подтвердите пароль:",
            font=("Arial", 12),
            fg="#4B0082",
            bg="#FFFFFF",
        ).pack()
        self.reg_confirm_password_entry = tk.Entry(
            self.root,
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
            self.root,
            text="Зарегистрироваться",
            font=("Arial", 12),
            bg="#4B0082",
            fg="white",
            relief="solid",
            command=self.registration,
        ).pack(pady=10)
        tk.Button(
            self.root,
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

        engine = create_db_engine()
        with get_db(engine) as db:
            message = register_user(db, username, password)

        if message == "Регистрация успешна! Теперь можно войти.":
            messagebox.showinfo("Успех", message)
            self.login_window()
        else:
            messagebox.showerror("Ошибка", message)

    def register_action(self, event=None):
        self.registration()
