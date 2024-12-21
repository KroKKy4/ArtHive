import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import io
import datetime

from const import (
    PROFILE_SCREEN_POST_COUNT,
    PROFILE_SCREEN_POST_WIDTH,
    PROFILE_SCREEN_POST_HEIGHT,
)


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
        top_frame.pack(fill="x", side="top")

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
        profile_info_frame.pack(pady=20)

        self.avatar_image = self.load_avatar(self.user.avatar)

        # Создаем Label для отображения аватара или заглушки
        avatar_label = tk.Label(
            profile_info_frame,
            image=self.avatar_image,  # type: ignore
            bg="#FFFFFF",
            relief="solid",
        )
        avatar_label.pack(padx=20, pady=10)

        # Кнопка для загрузки аватарки
        upload_avatar_button = tk.Button(
            profile_info_frame,
            text="Загрузить аватар",
            font=("Arial", 12),
            bg="#8A2BE2",
            fg="white",
            relief="solid",
            command=self.upload_avatar,  # Добавляем метод для загрузки аватарки
        )
        upload_avatar_button.pack(padx=20, pady=10)

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
        login_label.pack(padx=20, pady=10)

        # Кнопка изменения профиля
        edit_username_btn = tk.Button(
            profile_info_frame, text="Изменить имя", command=self.edit_username
        )
        edit_username_btn.pack(padx=10, pady=10)

        # Кнопка "Изменить пароль"
        edit_password_btn = tk.Button(
            profile_info_frame, text="Изменить пароль", command=self.edit_password
        )
        edit_password_btn.pack(padx=10, pady=10)

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
            command=self.create_publication_window,
        )
        create_publication_button.pack(side="left", padx=10, pady=5)

        published_posts_button = tk.Button(
            action_buttons_frame,
            text="Опубликованные посты",
            font=("Arial", 12),
            bg="#4B0082",
            fg="white",
            relief="solid",
            command=self.view_published_posts,
        )
        published_posts_button.pack(side="left", padx=10, pady=5)

        saved_posts_button = tk.Button(
            action_buttons_frame,
            text="Сохраненные посты",
            font=("Arial", 12),
            bg="#4B0082",
            fg="white",
            relief="solid",
            command=self.view_saved_posts,
        )
        saved_posts_button.pack(side="left", padx=10, pady=5)

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

    def edit_username(self):
        edit_window = tk.Toplevel(self.master)
        edit_window.title("Изменить имя пользователя")
        edit_window.geometry("400x200")
        edit_window.minsize(400, 200)

        # Метка и поле для нового имени
        username_label = tk.Label(
            edit_window, text="Новое имя пользователя:", font=("Arial", 12)
        )
        username_label.pack(pady=5)
        username_entry = tk.Entry(edit_window, font=("Arial", 12))
        username_entry.insert(0, self.user.username)  # Предзаполняем текущим именем
        username_entry.pack(pady=5)

        # Кнопка "Сохранить"
        def submit_username_changes():
            new_username = username_entry.get().strip()

            # Проверка, что поле заполнено
            if not new_username:
                messagebox.showerror("Ошибка", "Введите новое имя пользователя!")
                return

            # Проверка, что новое имя отличается от текущего
            if new_username == self.user.username:
                messagebox.showinfo("Информация", "Новое имя совпадает с текущим.")
                return

            try:
                updated_user = self.manager.user_crud.update_user(
                    username=self.user.username, new_username=new_username
                )
                messagebox.showinfo("Успех", "Имя пользователя успешно изменено!")

                # Обновляем данные в приложении
                self.manager.current_user = updated_user
                self.user = updated_user
                self.refresh_profile_data()

            except ValueError as e:
                messagebox.showerror("Ошибка", str(e))
            except Exception as e:
                messagebox.showerror("Ошибка", f"Произошла ошибка: {e}")
            finally:
                edit_window.destroy()

        tk.Button(
            edit_window,
            text="Сохранить",
            font=("Arial", 12),
            command=submit_username_changes,
        ).pack(pady=20)

    def edit_password(self):
        edit_window = tk.Toplevel(self.master)
        edit_window.title("Изменить пароль")
        edit_window.geometry("400x300")
        edit_window.minsize(300, 300)

        # Поле для ввода старого пароля
        old_password_label = tk.Label(
            edit_window, text="Старый пароль:", font=("Arial", 12)
        )
        old_password_label.pack(pady=5)
        old_password_entry = tk.Entry(edit_window, show="*", font=("Arial", 12))
        old_password_entry.pack(pady=5)

        # Поле для нового пароля
        new_password_label = tk.Label(
            edit_window, text="Новый пароль:", font=("Arial", 12)
        )
        new_password_label.pack(pady=5)
        new_password_entry = tk.Entry(edit_window, show="*", font=("Arial", 12))
        new_password_entry.pack(pady=5)

        # Кнопка "Сохранить"
        def submit_password_changes():
            old_password = old_password_entry.get().strip()
            new_password = new_password_entry.get().strip()

            # Проверка, что оба поля заполнены
            if not old_password or not new_password:
                messagebox.showerror("Ошибка", "Заполните старый и новый пароли!")
                return

            # Проверка старого пароля
            if not self.manager.user_crud.check_password(
                self.user.username, old_password
            ):
                messagebox.showerror("Ошибка", "Неверный старый пароль!")
                return

            # Проверка, что новый пароль отличается от старого
            if old_password == new_password:
                messagebox.showerror(
                    "Ошибка", "Новый пароль не должен совпадать со старым!"
                )
                return

            try:
                # Меняем только пароль, передаём новый пароль
                updated_user = self.manager.user_crud.update_user(
                    username=self.user.username, password=new_password
                )
                messagebox.showinfo("Успех", "Пароль успешно изменён!")

                # Обновляем данные в приложении
                self.manager.current_user = updated_user
                self.user = updated_user
                self.refresh_profile_data()

            except ValueError as e:
                messagebox.showerror("Ошибка", str(e))
            except Exception as e:
                messagebox.showerror("Ошибка", f"Произошла ошибка: {e}")
            finally:
                edit_window.destroy()

        tk.Button(
            edit_window,
            text="Сохранить",
            font=("Arial", 12),
            command=submit_password_changes,
        ).pack(pady=20)

    def create_publication_window(self):
        post_window = tk.Toplevel(self)
        post_window.title("Создать публикацию")
        post_window.geometry("550x550")

        tk.Label(post_window, text="Изображение:", font=("Arial", 12)).pack(pady=5)
        image_frame = tk.Frame(post_window)
        image_frame.pack(pady=5)

        image_path_var = tk.StringVar()

        # 1. Создаём "заглушку" (placeholder) через Pillow
        placeholder_image = Image.new("RGBA", (150, 150), (200, 200, 200, 255))
        placeholder_photo = ImageTk.PhotoImage(placeholder_image)

        # 2. Делаем Label для отображения выбранной картинки (или заглушки)
        preview_label = tk.Label(image_frame, image=placeholder_photo)  # type: ignore
        preview_label.image = (
            placeholder_photo  # чтобы изображение не "собиралось" сборщиком мусора
        )
        preview_label.pack(side="left", padx=10)

        def choose_image():
            filename = filedialog.askopenfilename(
                title="Выберите изображение для публикации",
                filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif")],
            )
            if filename:
                image_path_var.set(filename)
                # Загружаем картинку и уменьшаем до 150x150
                try:
                    img = Image.open(filename)
                    img = img.resize((150, 150), Image.Resampling.LANCZOS)
                    photo = ImageTk.PhotoImage(img)
                    # Обновляем Label, чтобы показывать выбранное изображение
                    preview_label.configure(image=photo)  # type: ignore
                    preview_label.image = photo
                except Exception as e:
                    messagebox.showerror(
                        "Ошибка", f"Не удалось загрузить картинку: {e}"
                    )

        # Кнопка «Выбрать изображение»
        tk.Button(image_frame, text="Выбрать изображение", command=choose_image).pack(
            side="top", padx=5
        )

        # Располагаем путь к файлу под кнопкой
        image_path_label = tk.Label(
            image_frame, textvariable=image_path_var, font=("Arial", 10)
        )
        image_path_label.pack(side="top", pady=5)

        tk.Label(post_window, text="Описание:", font=("Arial", 12)).pack(pady=5)
        description_text = tk.Text(post_window, width=50, height=5, font=("Arial", 12))
        description_text.pack(pady=5)

        tk.Label(
            post_window, text="Теги (до 5, разделите запятой):", font=("Arial", 12)
        ).pack(pady=5)
        tags_entry = tk.Entry(post_window, font=("Arial", 12))
        tags_entry.pack(pady=5)

        # Кнопка "Создать публикацию"
        create_button = tk.Button(
            post_window,
            text="Создать публикацию",
            bg="#4B0082",
            fg="white",
            font=("Arial", 12),
            command=lambda: create_post(),
        )
        create_button.pack(pady=20)

        # Привязка Enter для переходов
        description_text.bind("<Tab>", lambda e: tags_entry.focus())  # Переход на теги
        tags_entry.bind("<Return>", lambda e: create_button.focus())  # Переход к кнопке
        create_button.bind("<Return>", lambda e: create_post())  # Выполнение публикации

        def create_post():
            img_path = image_path_var.get().strip()
            description = description_text.get("1.0", tk.END).strip()
            tags_str = tags_entry.get().strip()

            if not img_path:
                messagebox.showerror("Ошибка", "Изображение не выбрано!")
                return

            try:
                with open(img_path, "rb") as f:
                    image_data = f.read()
            except Exception as e:
                messagebox.showerror(
                    "Ошибка", f"Не удалось прочитать файл изображения: {e}"
                )
                return

            tags = [t.strip() for t in tags_str.split(",") if t.strip()]
            if len(tags) > 5:
                messagebox.showerror("Ошибка", "Можно указать не более 5 тегов.")
                return

            try:
                new_image = self.manager.posts_crud.create_image_with_tags(
                    user_id=self.user.id,
                    image_data=image_data,
                    description=description,
                    tags=tags,
                    created_at=datetime.datetime.utcnow(),
                )

                # Показ успешного сообщения и возможность закрыть его Enter
                def close_message(event=None):
                    success_window.destroy()
                    post_window.destroy()

                success_window = tk.Toplevel(post_window)
                success_window.title("Успех")
                tk.Label(
                    success_window,
                    text="Публикация успешно создана!",
                    font=("Arial", 12),
                ).pack(pady=10)
                close_button = tk.Button(
                    success_window, text="Ок", command=close_message
                )
                close_button.pack(pady=10)
                success_window.bind("<Return>", close_message)
                success_window.focus_set()

            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось создать публикацию: {e}")

    def show_posts_in_window(self, title, posts):
        posts_window = tk.Toplevel(self)
        posts_window.title(title)
        posts_window.geometry("550x550")
        posts_window.minsize(520, 500)
        posts_window.maxsize(1200, 800)

        # Добавляем хоткей на Esc для закрытия окна
        posts_window.bind("<Escape>", lambda event: posts_window.destroy())

        if not posts:
            tk.Label(
                posts_window,
                text="Нет постов для отображения.",
                font=("Arial", 12),
            ).pack(pady=20)
            return

        container = tk.Frame(posts_window)
        container.pack(fill="both", expand=True)

        canvas = tk.Canvas(container)
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        canvas.configure(yscrollcommand=scrollbar.set)
        posts_frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=posts_frame, anchor="nw")

        def on_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        posts_frame.bind("<Configure>", on_configure)

        columns = PROFILE_SCREEN_POST_COUNT
        post_width = PROFILE_SCREEN_POST_WIDTH
        post_height = PROFILE_SCREEN_POST_HEIGHT

        for index, post in enumerate(posts):
            row = index // columns
            col = index % columns

            post_frame = tk.Frame(posts_frame, bd=2, relief="groove")
            post_frame.pack_propagate(False)
            post_frame.config(width=post_width, height=post_height)
            post_frame.grid(row=row, column=col, padx=5, pady=5, sticky="n")

            date_str = (
                post.created_at.strftime("%Y-%m-%d %H:%M")
                if post.created_at
                else "Без даты"
            )
            tk.Label(
                post_frame, text=f"Дата: {date_str}", font=("Arial", 10, "italic")
            ).pack(anchor="w", pady=(0, 5))

            desc = post.description if post.description else "Без описания"
            tk.Label(
                post_frame,
                text=desc,
                font=("Arial", 12),
                wraplength=200,
                justify="left",
            ).pack(anchor="w", pady=(0, 5))

            tag_names = [it.tag.name for it in post.tags] if post.tags else []
            if tag_names:
                tk.Label(
                    post_frame,
                    text="Теги: " + ", ".join(tag_names),
                    font=("Arial", 10, "italic"),
                ).pack(anchor="w", pady=(0, 5))

            if post.image_data:
                try:
                    img_data = io.BytesIO(post.image_data)
                    img = Image.open(img_data)
                    img = img.resize((150, 150), Image.Resampling.LANCZOS)
                    photo = ImageTk.PhotoImage(img)
                    img_label = tk.Label(post_frame, image=photo)  # type: ignore
                    img_label.image = photo
                    img_label.pack(anchor="w", pady=(5, 5))
                except Exception as e:
                    tk.Label(
                        post_frame,
                        text=f"Ошибка при загрузке изображения: {e}",
                        fg="red",
                    ).pack(anchor="w")

        tk.Button(posts_window, text="Закрыть", command=posts_window.destroy).pack(
            pady=10
        )

    def view_published_posts(self):
        user_posts = self.manager.posts_crud.get_user_images(self.user.id)
        self.show_posts_in_window("Опубликованные посты", user_posts)

    def view_saved_posts(self):
        saved_posts = self.manager.posts_crud.get_saved_posts_for_user(self.user.id)
        self.show_posts_in_window("Сохраненные посты", saved_posts)

    def load_avatar(self, avatar_bytes):
        if avatar_bytes:
            image_data = io.BytesIO(avatar_bytes)
            img = Image.open(image_data)
            img = img.resize((200, 200), Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(img)
        else:
            placeholder = Image.new("RGB", (200, 200), color="#8A2BE2")
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
