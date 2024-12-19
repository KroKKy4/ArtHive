import os
import tkinter as tk
from tkinter import messagebox, filedialog
import io
from PIL import Image, ImageTk
from tkinter import Tk


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

    def render_posts(self, posts):
        # Очищаем все элементы под строкой поиска
        for widget in self.winfo_children():
            if widget not in (self.search_entry.master,):
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
            canvas.configure(scrollregion=canvas.bbox("all"))

        all_posts_frame.bind("<Configure>", on_configure)

        # Добавляем поддержку прокрутки колесиком мыши
        def _on_mousewheel(event):
            # Для Windows
            if event.num == 4 or event.delta > 0:
                canvas.yview_scroll(-1, "units")
            elif event.num == 5 or event.delta < 0:
                canvas.yview_scroll(1, "units")

        # Привязки для разных систем
        # Windows:
        canvas.bind("<MouseWheel>", _on_mousewheel)
        # Linux (обычно требуется):
        canvas.bind("<Button-4>", _on_mousewheel)
        canvas.bind("<Button-5>", _on_mousewheel)

        if not posts:
            tk.Label(
                all_posts_frame, text="Нет постов для отображения.", font=("Arial", 12)
            ).pack(pady=20)
            return

        # Настраиваем параметры сетки
        columns = 4
        POST_WIDTH = 250
        POST_HEIGHT = 300

        total_columns = columns + 2
        all_posts_frame.grid_columnconfigure(0, weight=1)
        all_posts_frame.grid_columnconfigure(total_columns - 1, weight=1)

        # Создаём карточки постов
        for index, post in enumerate(posts):
            row = index // columns
            col = (index % columns) + 1

            post_frame = tk.Frame(all_posts_frame, bd=2, relief="groove")
            post_frame.pack_propagate(False)
            post_frame.config(width=POST_WIDTH, height=POST_HEIGHT)
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
        posts = self.manager.image_crud.get_all_images()
        self.render_posts(posts)

    def show_filtered_posts(self, posts):
        self.render_posts(posts)

    def show_post_details(self, post):
        # Создаём новое окно с деталями поста
        detail_window = tk.Toplevel(self)
        detail_window.title("Детали поста")
        detail_window.geometry("800x750")  # Устанавливаем фиксированный размер
        detail_window.resizable(False, False)  # Отключаем изменение размеров окна

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
            found_posts = self.manager.image_crud.search_posts_by_tags(search_query)
            if not found_posts:
                messagebox.showinfo("Поиск", "Постов с таким хэштегом не найдено.")
                return
            self.show_filtered_posts(found_posts)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось выполнить поиск: {e}")

    def show_profile(self):
        self.manager.show_profile_interface(self.user)

    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()
