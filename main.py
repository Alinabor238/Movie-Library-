import json
import os
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox


class MovieLibrary:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Library - Личная кинотека")
        self.root.geometry("900x600")

        # Хранилище фильмов
        self.movies = []
        self.filtered_movies = []

        # Загрузка данных из JSON
        self.load_data()

        # Создание интерфейса
        self.create_widgets()

        # Обновление таблицы
        self.refresh_table()

        # Сохранение при закрытии
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_widgets(self):
        # Рамка для ввода данных
        input_frame = ttk.LabelFrame(self.root, text="Добавление фильма", padding=10)
        input_frame.pack(fill="x", padx=10, pady=5)

        # Поля ввода
        ttk.Label(input_frame, text="Название:").grid(row=0, column=0, sticky="w", padx=5)
        self.title_entry = ttk.Entry(input_frame, width=30)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Жанр:").grid(row=0, column=2, sticky="w", padx=5)
        self.genre_entry = ttk.Entry(input_frame, width=20)
        self.genre_entry.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(input_frame, text="Год выпуска:").grid(row=1, column=0, sticky="w", padx=5)
        self.year_entry = ttk.Entry(input_frame, width=30)
        self.year_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Рейтинг (0-10):").grid(row=1, column=2, sticky="w", padx=5)
        self.rating_entry = ttk.Entry(input_frame, width=20)
        self.rating_entry.grid(row=1, column=3, padx=5, pady=5)

        # Кнопка добавления
        self.add_button = ttk.Button(input_frame, text="Добавить фильм", command=self.add_movie)
        self.add_button.grid(row=2, column=0, columnspan=4, pady=10)

        # Рамка для фильтрации
        filter_frame = ttk.LabelFrame(self.root, text="Фильтрация", padding=10)
        filter_frame.pack(fill="x", padx=10, pady=5)

        # Фильтр по жанру
        ttk.Label(filter_frame, text="Фильтр по жанру:").grid(row=0, column=0, sticky="w", padx=5)
        self.genre_filter = ttk.Combobox(filter_frame, width=20)
        self.genre_filter.grid(row=0, column=1, padx=5, pady=5)
        self.update_genre_list()

        # Фильтр по году
        ttk.Label(filter_frame, text="Фильтр по году (минимум):").grid(row=0, column=2, sticky="w", padx=5)
        self.year_filter = ttk.Entry(filter_frame, width=10)
        self.year_filter.grid(row=0, column=3, padx=5, pady=5)

        # Кнопки фильтрации
        self.apply_filter_button = ttk.Button(filter_frame, text="Применить фильтр", command=self.apply_filter)
        self.apply_filter_button.grid(row=0, column=4, padx=5)

        self.reset_filter_button = ttk.Button(filter_frame, text="Сбросить фильтр", command=self.reset_filter)
        self.reset_filter_button.grid(row=0, column=5, padx=5)

        # Таблица для отображения фильмов
        table_frame = ttk.LabelFrame(self.root, text="Список фильмов", padding=10)
        table_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Создание таблицы
        columns = ("Название", "Жанр", "Год", "Рейтинг")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)

        # Настройка заголовков
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=200)

        # Добавление скроллбара
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Информационная строка
        self.info_label = ttk.Label(self.root, text="Всего фильмов: 0", font=("Arial", 10))
        self.info_label.pack(pady=5)

    def add_movie(self):
        # Получение данных из полей
        title = self.title_entry.get().strip()
        genre = self.genre_entry.get().strip()
        year_str = self.year_entry.get().strip()
        rating_str = self.rating_entry.get().strip()

        # Проверка названия
        if not title:
            messagebox.showerror("Ошибка", "Название фильма не может быть пустым!")
            return

        # Проверка года
        try:
            year = int(year_str)
            current_year = datetime.now().year
            if year < 1888 or year > current_year:
                messagebox.showerror("Ошибка", f"Год должен быть от 1888 до {current_year}!")
                return
        except ValueError:
            messagebox.showerror("Ошибка", "Год должен быть числом!")
            return

        # Проверка рейтинга
        try:
            rating = float(rating_str)
            if rating < 0 or rating > 10:
                messagebox.showerror("Ошибка", "Рейтинг должен быть от 0 до 10!")
                return
        except ValueError:
            messagebox.showerror("Ошибка", "Рейтинг должен быть числом!")
            return

        # Проверка жанра
        if not genre:
            messagebox.showerror("Ошибка", "Жанр не может быть пустым!")
            return

        # Добавление фильма
        movie = {
            "title": title,
            "genre": genre,
            "year": year,
            "rating": rating
        }

        self.movies.append(movie)
        self.update_genre_list()
        self.reset_filter()
        self.refresh_table()

        # Очистка полей
        self.title_entry.delete(0, tk.END)
        self.genre_entry.delete(0, tk.END)
        self.year_entry.delete(0, tk.END)
        self.rating_entry.delete(0, tk.END)

        messagebox.showinfo("Успех", f"Фильм '{title}' успешно добавлен!")

    def apply_filter(self):
        genre_filter = self.genre_filter.get().strip()
        year_filter_str = self.year_filter.get().strip()

        self.filtered_movies = self.movies.copy()

        # Фильтрация по жанру
        if genre_filter:
            self.filtered_movies = [m for m in self.filtered_movies if m["genre"].lower() == genre_filter.lower()]

        # Фильтрация по году
        if year_filter_str:
            try:
                year_filter = int(year_filter_str)
                self.filtered_movies = [m for m in self.filtered_movies if m["year"] >= year_filter]
            except ValueError:
                messagebox.showerror("Ошибка", "Год для фильтрации должен быть числом!")
                return

        self.refresh_table(use_filtered=True)

    def reset_filter(self):
        self.genre_filter.set("")
        self.year_filter.delete(0, tk.END)
        self.filtered_movies = []
        self.refresh_table()

    def refresh_table(self, use_filtered=False):
        # Очистка таблицы
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Выбор данных для отображения
        display_movies = self.filtered_movies if use_filtered and self.filtered_movies else self.movies

        # Заполнение таблицы
        for movie in display_movies:
            self.tree.insert("", tk.END, values=(
                movie["title"],
                movie["genre"],
                movie["year"],
                f"{movie['rating']:.1f}"
            ))

        # Обновление информационной строки
        total = len(self.movies)
        displayed = len(display_movies)
        if use_filtered and self.filtered_movies and total != displayed:
            self.info_label.config(text=f"Всего фильмов: {total} (Показано: {displayed})")
        else:
            self.info_label.config(text=f"Всего фильмов: {total}")

    def update_genre_list(self):
        # Получение уникальных жанров
        genres = sorted(set(m["genre"] for m in self.movies))
        self.genre_filter["values"] = [""] + genres

    def load_data(self):
        """Загрузка данных из JSON файла"""
        if os.path.exists("movies.json"):
            try:
                with open("movies.json", "r", encoding="utf-8") as file:
                    self.movies = json.load(file)
            except (json.JSONDecodeError, IOError) as e:
                messagebox.showwarning("Предупреждение", f"Не удалось загрузить данные: {e}")
                self.movies = []

    def save_data(self):
        """Сохранение данных в JSON файл"""
        try:
            with open("movies.json", "w", encoding="utf-8") as file:
                json.dump(self.movies, file, ensure_ascii=False, indent=2)
        except IOError as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить данные: {e}")

    def on_closing(self):
        """Действие при закрытии окна"""
        self.save_data()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = MovieLibrary(root)
    root.mainloop()