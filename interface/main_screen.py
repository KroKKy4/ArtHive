import tkinter as tk
from tkinter import messagebox

from db.models import User


class MainInterface(tk.Frame):
    def __init__(self, master, manager, user, *args, **kwargs):
        super().__init__(master)
        self.search_entry = None
        self.manager = manager
        self.user = user
        self.main_window()

    def main_window(self):
        self.clear_window()
        top_frame = tk.Frame(self, bg="#FFFFFF")
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

        search_button = tk.Button(
            top_frame,
            text="Найти",
            font=("Arial", 12),
            bg="#4B0082",
            fg="white",
            relief="solid",
            command=self.search_images,
        )
        search_button.pack(side="left", padx=10)

        profile_button = tk.Button(
            top_frame,
            text="Профиль",
            font=("Arial", 12),
            bg="#8A2BE2",
            fg="white",
            relief="solid",
            command=self.show_profile,
        )
        profile_button.pack(side="right", padx=10)

        self.pack(fill=tk.BOTH, expand=True)

    def show_profile(self):
        self.manager.show_profile_interface(self.user)

    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()

    def search_images(self):
        search_query = self.search_entry.get()
        messagebox.showinfo("Поиск", f"Вы искали: {search_query}")

    @staticmethod
    def on_mouse_wheel(event, canvas):
        """Handle mouse wheel scroll."""
        canvas.yview_scroll(-1 * (event.delta // 120), "units")
