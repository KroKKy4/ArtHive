import tkinter as tk
from tkinter import messagebox

from db.models import User


class ProfileInterface(tk.Frame):
    def __init__(self, master, manager, user, main_window_callback, *args, **kwargs):
        super().__init__(master)
        self.manager = manager
        self.main_window_callback = main_window_callback
        self.user = user
        self.show_profile()

    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()

    def show_profile(self):
        self.clear_window()

        # Создаём canvas с прокруткой
        canvas = tk.Canvas(self, width=900, height=600)
        canvas.pack(side="left", fill="both", expand=True)

        # Добавляем вертикальный скроллбар
        scrollbar = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        canvas.configure(yscrollcommand=scrollbar.set)

        # Привязываем колесо мыши к прокрутке canvas
        canvas.bind_all(
            "<MouseWheel>", lambda event: self.on_mouse_wheel(event, canvas)
        )

        # Создаем фрейм внутри canvas для профиля
        profile_frame = tk.Frame(canvas, bg="#FFFFFF")
        canvas.create_window((0, 0), window=profile_frame, anchor="nw", width=900)

        # Добавляем виджеты в профиль
        top_frame = tk.Frame(profile_frame, bg="#FFFFFF")
        top_frame.pack(fill="x", pady=10)

        back_button = tk.Button(
            top_frame,
            text="← Назад",
            font=("Arial", 12),
            bg="#4B0082",
            fg="white",
            relief="solid",
            command=self.main_window_callback,
        )
        back_button.pack(side="left", padx=10)

        logout_button = tk.Button(
            top_frame,
            text="Выйти",
            font=("Arial", 12),
            bg="#8A2BE2",
            fg="white",
            relief="solid",
            command=self.logout,
        )
        logout_button.pack(side="right", padx=10)

        profile_frame_inner = tk.Frame(profile_frame, bg="#FFFFFF")
        profile_frame_inner.pack(pady=20)

        avatar_label = tk.Label(
            profile_frame_inner,
            text="Аватар",
            font=("Arial", 12, "bold"),
            bg="#8A2BE2",
            fg="white",
            width=8,
            height=4,
            relief="solid",
            anchor="center",
        )
        avatar_label.grid(row=0, column=0, padx=20, pady=10)

        if isinstance(self.user, User):
            username_display = self.user.username
        else:
            print("self.user is not a User instance:", self.user)
            username_display = "Unknown User"

        login_label = tk.Label(
            profile_frame_inner,
            text=username_display,
            font=("Arial", 20),
            fg="#4B0082",
            bg="#FFFFFF",
        )
        login_label.grid(row=0, column=1, padx=20, pady=10, sticky="w")

        button_frame = tk.Frame(profile_frame, bg="#FFFFFF")
        button_frame.pack(pady=10)

    @staticmethod
    def on_mouse_wheel(event, canvas):
        """Handle mouse wheel scroll."""
        canvas.yview_scroll(-1 * (event.delta // 120), "units")

    def logout(self):
        response = messagebox.askyesno("Выход", "Вы уверены, что хотите выйти?")
        if response:
            self.clear_window()
            self.manager.logout_success()
