import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
from PIL import Image, ImageTk
import io


class ProfileInterface(tk.Frame):
    def __init__(self, master, manager, user, main_window_callback, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.avatar_image = None
        self.manager = manager
        self.user = user or self.manager.current_user
        self.main_window_callback = main_window_callback
        self.canvas = None

        # Настраиваем внешний контейнер
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Создаём фрейм для содержимого
        self.content_frame = tk.Frame(self, bg="#FFFFFF")
        self.content_frame.grid(row=0, column=0, sticky="nsew")

        # Создаём интерфейс
        self.create_widgets()

    def create_top_frame(self):
        top_frame = tk.Frame(self.content_frame, bg="#FFFFFF")
        top_frame.pack(fill="x", side="top")  # Растягиваем по горизонтали

        # Фрейм для кнопки "Назад"
        left_frame = tk.Frame(top_frame, bg="#FFFFFF")
        left_frame.pack(side="left", fill="y")

        back_button = tk.Button(
            left_frame,
            text="← Назад",
            font=("Arial", 12),
            bg="#4B0082",
            fg="white",
            relief="solid",
            command=self.main_window_callback,
        )
        back_button.pack(padx=10, pady=5)

        # Фрейм для кнопки "Выйти"
        right_frame = tk.Frame(top_frame, bg="#FFFFFF")
        right_frame.pack(side="right", fill="y")

        logout_button = tk.Button(
            right_frame,
            text="Выйти",
            font=("Arial", 12),
            bg="#8A2BE2",
            fg="white",
            relief="solid",
            command=self.logout,
        )
        logout_button.pack(padx=10, pady=5)

    def create_widgets(self):
        # Верхняя панель
        self.create_top_frame()

        # Фрейм для содержимого профиля
        profile_info_frame = tk.Frame(self.content_frame, bg="#FFFFFF")
        profile_info_frame.pack(pady=20, expand=True)

        self.avatar_image = self.load_avatar(self.user.avatar)

        # Создаем Label для отображения аватара или заглушки
        avatar_label = tk.Label(
            profile_info_frame,
            image=self.avatar_image,  # type: ignore
            bg="#FFFFFF",
            relief="solid",
        )
        avatar_label.grid(row=0, column=0, padx=20, pady=10)

        # Кнопка для загрузки нового аватара
        upload_button = tk.Button(
            profile_info_frame,
            text="Загрузить аватар",
            font=("Arial", 12),
            bg="#8A2BE2",
            fg="white",
            relief="solid",
            command=self.upload_avatar,
        )
        upload_button.grid(row=1, column=0, padx=10, pady=5)

        # Отображение имени пользователя
        username_display = (
            self.user.username if hasattr(self.user, "username") else "Unknown User"
        )
        login_label = tk.Label(
            profile_info_frame,
            text=username_display,
            font=("Arial", 20),
            fg="#4B0082",
            bg="#FFFFFF",
        )
        login_label.grid(row=0, column=1, padx=20, pady=10, sticky="w")

        # Кнопка изменения профиля
        edit_profile_button = tk.Button(
            profile_info_frame,
            text="Изменить данные профиля",
            font=("Arial", 12),
            bg="#8A2BE2",
            fg="white",
            relief="solid",
            command=self.edit_profile,
        )
        edit_profile_button.grid(row=1, column=1, padx=20, pady=10)

        # Кнопки для действий
        action_buttons_frame = tk.Frame(self.content_frame, bg="#FFFFFF")
        action_buttons_frame.pack(pady=20)

        create_publication_button = tk.Button(
            action_buttons_frame,
            text="Создать публикацию",
            font=("Arial", 12),
            bg="#4B0082",
            fg="white",
            relief="solid",
            command=self.create_publication,
        )
        create_publication_button.grid(row=0, column=0, padx=10, pady=5)

        published_posts_button = tk.Button(
            action_buttons_frame,
            text="Опубликованные посты",
            font=("Arial", 12),
            bg="#4B0082",
            fg="white",
            relief="solid",
            command=self.view_published_posts,
        )
        published_posts_button.grid(row=0, column=1, padx=10, pady=5)

        saved_posts_button = tk.Button(
            action_buttons_frame,
            text="Сохраненные посты",
            font=("Arial", 12),
            bg="#4B0082",
            fg="white",
            relief="solid",
            command=self.view_saved_posts,
        )
        saved_posts_button.grid(row=0, column=2, padx=10, pady=5)

    def on_mousewheel(self, event):
        self.canvas.yview_scroll(-1 * (event.delta // 120), "units")

    def logout(self):
        response = messagebox.askyesno("Выход", "Вы уверены, что хотите выйти?")
        if response:
            self.manager.logout_success()

    def refresh_profile_data(self):
        self.content_frame.destroy()
        self.content_frame = tk.Frame(self, bg="#FFFFFF")
        self.content_frame.grid(row=0, column=0, sticky="nsew")
        self.create_widgets()

    def edit_profile(self):
        edit_window = tk.Toplevel(self)
        edit_window.title("Изменить профиль")
        edit_window.geometry("400x250")

        tk.Label(edit_window, text="Новое имя пользователя:", font=("Arial", 12)).pack(
            pady=10
        )
        username_entry = tk.Entry(edit_window, font=("Arial", 12))
        username_entry.pack(pady=5)

        tk.Label(edit_window, text="Новый пароль:", font=("Arial", 12)).pack(pady=10)
        password_entry = tk.Entry(edit_window, font=("Arial", 12), show="*")
        password_entry.pack(pady=5)

        def submit_changes():
            new_username = username_entry.get().strip()
            new_password = password_entry.get().strip()

            if not new_username and not new_password:
                messagebox.showerror("Ошибка", "Заполните хотя бы одно поле!")
                return

            try:
                updated_user = self.manager.user_crud.update_user(
                    self.user.username, new_username=new_username, password=new_password
                )
                messagebox.showinfo("Успех", "Данные успешно изменены!")

                # Обновляем текущего пользователя в менеджере
                self.manager.current_user = updated_user
                self.user = updated_user  # Локальное обновление
                self.refresh_profile_data()  # Перезагружаем интерфейс профиля
            except ValueError as e:
                messagebox.showerror("Ошибка", str(e))
            except Exception as e:
                messagebox.showerror("Ошибка", f"Произошла ошибка: {e}")
            finally:
                edit_window.destroy()

        tk.Button(
            edit_window, text="Сохранить", font=("Arial", 12), command=submit_changes
        ).pack(pady=20)

    def create_publication(self):
        messagebox.showinfo(
            "Создание публикации", "Функция создания публикации в разработке."
        )

    def view_published_posts(self):
        messagebox.showinfo(
            "Опубликованные посты",
            "Функция просмотра опубликованных постов в разработке.",
        )

    def view_saved_posts(self):
        messagebox.showinfo(
            "Сохраненные посты", "Функция просмотра сохраненных постов в разработке."
        )

    def load_avatar(self, avatar_bytes):
        if avatar_bytes:
            # Если аватар есть, конвертируем байты в изображение
            image_data = io.BytesIO(avatar_bytes)
            img = Image.open(image_data)
            # Опционально можем изменить размер аватара, например до 100x100
            img = img.resize((100, 100), Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(img)
        else:
            placeholder = Image.new("RGB", (100, 100), color="#8A2BE2")
            return ImageTk.PhotoImage(placeholder)

    def upload_avatar(self):
        filename = filedialog.askopenfilename(
            title="Выберите изображение для аватара",
            filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif")],
        )
        if filename:
            try:
                with open(filename, "rb") as f:
                    avatar_data = f.read()
                # Обновляем пользователя
                updated_user = self.manager.user_crud.update_user(
                    self.user.username, avatar=avatar_data
                )
                self.manager.current_user = updated_user
                self.user = updated_user
                messagebox.showinfo("Успех", "Аватар успешно обновлён!")
                self.refresh_profile_data()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить аватар: {e}")
