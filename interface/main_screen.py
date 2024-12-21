import os
import tkinter as tk
from tkinter import messagebox, filedialog
import io
from PIL import Image, ImageTk
from tkinter import Tk

from const import (
    MAIN_SCREEN_POST_WIDTH,
    MAIN_SCREEN_POST_HEIGHT,
    MAIN_SCREEN_POST_COUNT,
)


# TODO при изменении пароля добавить проверку на текущий пароль +
# TODO изменить цвет топ фрейма F0F0F0 +
# TODO убрать нумерацию постов в "Опубликованные посты" +
# TODO изменить разрешение окна "Опубликованные посты" +
# TODO какие ошибки и сложности были в проекте - Цикличные импорты, сохранение картинок на компьютер пользователя,
#                                                   передача данных пользователей в разные интерфейсы +
# TODO добавить очистку поля поиска после нажатия на кнопку +

# TODO попробовать добавить функционал с перекрытием окна
# TODO добавить пагинацию
# TODO добавить 2 хоткея один для esc(назад) и enter для поиска
# TODO enter для перехода между полями в авторизации
# TODO переход от тэгов к подтверждению создания публикации с помощью enter
# TODO закрытие окна на enter или esc для "Опубликованные посты"
# TODO добавить микро аватарку в создание поста


class MainInterface(tk.Frame):
    def __init__(self, master: Tk, manager, user, *args, **kwargs):
        super().__init__(master)
        self.search_entry = None
        self.manager = manager
        self.user = user
        self.main_window()

    def main_window(self):
        # Устанавливаем фиксированный размер окна
        self.master.geometry("1060x700")  # Увеличиваем ширину окна
        self.master.resizable(False, False)  # Отключаем изменение размеров окна

        self.clear_window()
        top_frame = tk.Frame(self, bg="#F0F0F0")
        top_frame.pack(fill="x", pady=10)

        search_label = tk.Label(
            top_frame,
            text="Поиск изображений:",
            font=("Arial", 12),
            fg="#4B0082",
            bg="#F0F0F0",
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

        show_all_button = tk.Button(
            top_frame,
            text="Показать все посты",
            font=("Arial", 12),
            bg="#8A2BE2",
            fg="white",
            relief="solid",
            command=self.show_all_posts,
        )
        show_all_button.pack(side="right", padx=10)

        self.show_all_posts()
        self.pack(fill=tk.BOTH, expand=True)

        # Устанавливаем хоткеи
        self.setup_hotkeys()

    def render_posts(self, posts):
        # Очищаем все элементы под строкой поиска
        for widget in self.winfo_children():
            if widget != self.search_entry.master:
                widget.destroy()

        posts_container = tk.Frame(self)
        posts_container.pack(fill="both", expand=True)

        canvas = tk.Canvas(posts_container)
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(
            posts_container, orient="vertical", command=canvas.yview
        )
        scrollbar.pack(side="right", fill="y")

        canvas.configure(yscrollcommand=scrollbar.set)
        all_posts_frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=all_posts_frame, anchor="nw")

        def on_configure(event):
            # Установка границ прокрутки
            canvas.configure(scrollregion=canvas.bbox("all"))

        all_posts_frame.bind("<Configure>", on_configure)

        # Добавляем поддержку прокрутки колесиком мыши
        def _on_mousewheel(event):
            if event.delta:  # Windows и macOS
                canvas.yview_scroll(-1 * (event.delta // 120), "units")
            elif event.num in (4, 5):  # Linux
                canvas.yview_scroll(-1 if event.num == 4 else 1, "units")

        # Привязки событий только для области canvas
        canvas.bind("<Enter>", lambda _: canvas.bind("<MouseWheel>", _on_mousewheel))
        canvas.bind("<Leave>", lambda _: canvas.unbind("<MouseWheel>"))
        canvas.bind("<Enter>", lambda _: canvas.bind("<Button-4>", _on_mousewheel))
        canvas.bind("<Enter>", lambda _: canvas.bind("<Button-5>", _on_mousewheel))
        canvas.bind("<Leave>", lambda _: canvas.unbind("<Button-4>"))
        canvas.bind("<Leave>", lambda _: canvas.unbind("<Button-5>"))

        if not posts:
            tk.Label(
                all_posts_frame, text="Нет постов для отображения.", font=("Arial", 12)
            ).pack(pady=20)
            return

        columns = MAIN_SCREEN_POST_COUNT
        post_width = MAIN_SCREEN_POST_WIDTH
        post_height = MAIN_SCREEN_POST_HEIGHT

        total_columns = columns + 2
        all_posts_frame.grid_columnconfigure(0, weight=1)
        all_posts_frame.grid_columnconfigure(total_columns - 1, weight=1)

        # Создаём карточки постов
        for index, post in enumerate(posts):
            row = index // columns
            col = (index % columns) + 1

            post_frame = tk.Frame(all_posts_frame, bd=2, relief="groove")
            post_frame.pack_propagate(False)
            post_frame.config(width=post_width, height=post_height)
            post_frame.grid(row=row, column=col, padx=5, pady=5, sticky="n")

            if post.image_data:
                try:
                    img_data = io.BytesIO(post.image_data)
                    img = Image.open(img_data)
                    img.thumbnail((200, 150), Image.Resampling.LANCZOS)
                    photo = ImageTk.PhotoImage(img)
                    img_label = tk.Label(post_frame, image=photo)  # type: ignore
                    img_label.image = photo
                    img_label.pack(anchor="center", pady=(5, 5))
                except Exception as e:
                    tk.Label(
                        post_frame,
                        text=f"Ошибка при загрузке изображения: {e}",
                        fg="red",
                    ).pack(anchor="w")
            else:
                tk.Label(post_frame, text="Нет изображения", fg="gray").pack(
                    anchor="center", pady=50
                )

            author_name = post.user.username if post.user else "Неизвестный автор"
            tk.Label(post_frame, text=f"Автор: {author_name}", font=("Arial", 10)).pack(
                anchor="center", pady=5
            )

            view_button = tk.Button(
                post_frame,
                text="Перейти к посту",
                bg="#4B0082",
                fg="white",
                relief="solid",
                command=lambda p=post: self.show_post_details(p),
            )
            view_button.pack(anchor="center", pady=5)

    def show_all_posts(self):
        posts = self.manager.posts_crud.get_all_images()
        self.render_posts(posts)

    def show_filtered_posts(self, posts):
        self.render_posts(posts)

    def show_post_details(self, post):
        detail_window = tk.Toplevel(self)
        detail_window.title("Детали поста")
        detail_window.geometry("800x750")
        detail_window.resizable(False, False)

        if post.image_data:
            try:
                img_data = io.BytesIO(post.image_data)
                img = Image.open(img_data)
                img.thumbnail((700, 400), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                img_label = tk.Label(detail_window, image=photo)  # type: ignore
                img_label.image = photo
                img_label.pack(pady=(10, 20))
            except Exception as e:
                tk.Label(
                    detail_window,
                    text=f"Ошибка при загрузке изображения: {e}",
                    fg="red",
                ).pack(anchor="w", pady=(5, 10))

        desc = post.description if post.description else "Без описания"
        tk.Label(detail_window, text="Описание:", font=("Arial", 12, "bold")).pack(
            anchor="w", padx=10, pady=(5, 0)
        )
        tk.Label(
            detail_window, text=desc, font=("Arial", 12), wraplength=700, justify="left"
        ).pack(anchor="w", padx=10, pady=(0, 10))

        author_name = post.user.username if post.user else "Неизвестный автор"
        tk.Label(detail_window, text=f"Автор: {author_name}", font=("Arial", 12)).pack(
            anchor="w", padx=10, pady=(0, 10)
        )

        tag_names = [it.tag.name for it in post.tags] if post.tags else []
        if tag_names:
            tk.Label(detail_window, text="Теги:", font=("Arial", 12, "bold")).pack(
                anchor="w", padx=10, pady=(0, 5)
            )
            tk.Label(
                detail_window,
                text=", ".join(tag_names),
                font=("Arial", 10),
                wraplength=700,
                justify="left",
            ).pack(anchor="w", padx=10, pady=(0, 20))

        def download_image():
            if not post.image_data or not isinstance(post.image_data, bytes):
                messagebox.showerror(
                    "Ошибка", "Данные изображения отсутствуют или некорректны."
                )
                return

            save_path = filedialog.asksaveasfilename(
                title="Сохранить изображение",
                defaultextension=".jpg",
                filetypes=[
                    ("JPEG", "*.jpg"),
                    ("PNG", "*.png"),
                    ("All Files", "*.*"),
                ],
                initialdir="C:\\",  # Можно задать начальную директорию, например корень диска
            )
            if not save_path:
                return

            dir_path = os.path.dirname(save_path)
            if dir_path and not os.path.exists(dir_path):
                try:
                    os.makedirs(dir_path, exist_ok=True)
                except Exception as e:
                    messagebox.showerror(
                        "Ошибка", f"Не удалось создать директорию: {e}"
                    )
                    return

            try:
                with open(save_path, "wb") as f:
                    f.write(post.image_data)
                messagebox.showinfo(
                    "Успех", f"Изображение успешно сохранено в {save_path}."
                )
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить изображение: {e}")

        download_button = tk.Button(
            detail_window,
            text="Скачать картинку",
            bg="#4B0082",
            fg="white",
            relief="solid",
            command=download_image,
        )
        download_button.pack(pady=(10, 20))

        def save_post():
            try:
                self.manager.posts_crud.save_post_for_user(self.user.id, post.id)
                messagebox.showinfo("Успех", "Пост успешно сохранён!")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить пост: {e}")

        # Кнопка "Сохранить пост"
        save_button = tk.Button(
            detail_window,
            text="Сохранить пост",
            bg="#4B0082",
            fg="white",
            relief="solid",
            command=save_post,
        )
        save_button.pack(pady=(0, 20))

        close_button = tk.Button(
            detail_window, text="Закрыть", command=detail_window.destroy
        )
        close_button.pack(pady=10)

    def search_images(self):
        search_query = self.search_entry.get().strip()

        if not search_query:
            messagebox.showwarning("Поиск", "Введите хэштег для поиска.")
            return

        try:
            found_posts = self.manager.posts_crud.search_posts_by_tags(search_query)
            if not found_posts:
                messagebox.showinfo("Поиск", "Постов с таким хэштегом не найдено.")
                return

            self.show_filtered_posts(found_posts)

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось выполнить поиск: {e}")
        finally:
            # Очищаем поле поиска в любом случае (успешный поиск, неудачный или исключение)
            self.search_entry.delete(0, tk.END)

    def show_profile(self):
        self.manager.show_profile_interface(self.user)

    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()

    def setup_hotkeys(self):
        # Переход в профиль по Ctrl+P
        self.master.bind_all("<Control-p>", lambda event: self.show_profile())
        # Поиск постов по Ctrl+F
        self.master.bind_all("<Control-f>", lambda event: self.focus_search())
        # Показ всех постов по Ctrl+A
        self.master.bind_all("<Control-a>", lambda event: self.show_all_posts())
        # Закрытие приложения по Ctrl+Q
        self.master.bind_all("<Control-q>", lambda event: self.master.destroy())
        # Привязка нажатия Enter к строке поиска
        self.search_entry.bind("<Return>", lambda event: self.search_images())

    def focus_search(self):
        if self.search_entry:
            self.search_entry.focus_set()
