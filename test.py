import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json

class BookTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Book Tracker")

        self.books = []

        # --- Form ---
        tk.Label(root, text="Название").grid(row=0, column=0)
        tk.Label(root, text="Автор").grid(row=1, column=0)
        tk.Label(root, text="Жанр").grid(row=2, column=0)
        tk.Label(root, text="Страницы").grid(row=3, column=0)

        self.title_entry = tk.Entry(root)
        self.author_entry = tk.Entry(root)
        self.genre_entry = tk.Entry(root)
        self.pages_entry = tk.Entry(root)

        self.title_entry.grid(row=0, column=1)
        self.author_entry.grid(row=1, column=1)
        self.genre_entry.grid(row=2, column=1)
        self.pages_entry.grid(row=3, column=1)

        tk.Button(root, text="Добавить книгу", command=self.add_book).grid(row=4, column=0, columnspan=2, pady=5)

        # --- Filters ---
        tk.Label(root, text="Фильтр по жанру").grid(row=5, column=0)
        self.genre_filter = tk.Entry(root)
        self.genre_filter.grid(row=5, column=1)

        tk.Button(root, text="Фильтр по жанру", command=self.apply_genre_filter).grid(row=6, column=0, columnspan=2)

        tk.Label(root, text="Страниц больше чем").grid(row=7, column=0)
        self.pages_filter = tk.Entry(root)
        self.pages_filter.grid(row=7, column=1)

        tk.Button(root, text="Фильтр по страницам", command=self.apply_pages_filter).grid(row=8, column=0, columnspan=2)

        tk.Button(root, text="Сбросить фильтры", command=self.reset_filters).grid(row=9, column=0, columnspan=2)

        # --- Table ---
        self.tree = ttk.Treeview(root, columns=("Title", "Author", "Genre", "Pages"), show="headings")
        for col in ("Title", "Author", "Genre", "Pages"):
            self.tree.heading(col, text=col)
        self.tree.grid(row=10, column=0, columnspan=2)

        # --- JSON buttons ---
        tk.Button(root, text="Сохранить JSON", command=self.save_json).grid(row=11, column=0)
        tk.Button(root, text="Загрузить JSON", command=self.load_json).grid(row=11, column=1)

    def add_book(self):
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        genre = self.genre_entry.get().strip()
        pages = self.pages_entry.get().strip()

        if not title or not author or not genre or not pages:
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены")
            return

        if not pages.isdigit():
            messagebox.showerror("Ошибка", "Страницы должны быть числом")
            return

        book = {
            "title": title,
            "author": author,
            "genre": genre,
            "pages": int(pages)
        }

        self.books.append(book)
        self.update_table(self.books)
        self.clear_fields()

    def update_table(self, data):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for book in data:
            self.tree.insert("", "end", values=(book["title"], book["author"], book["genre"], book["pages"]))

    def clear_fields(self):
        self.title_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.genre_entry.delete(0, tk.END)
        self.pages_entry.delete(0, tk.END)

    def apply_genre_filter(self):
        genre = self.genre_filter.get().strip().lower()
        filtered = [b for b in self.books if b["genre"].lower() == genre]
        self.update_table(filtered)

    def apply_pages_filter(self):
        pages = self.pages_filter.get().strip()

        if not pages.isdigit():
            messagebox.showerror("Ошибка", "Введите число страниц")
            return

        pages = int(pages)
        filtered = [b for b in self.books if b["pages"] > pages]
        self.update_table(filtered)

    def reset_filters(self):
        self.update_table(self.books)

    def save_json(self):
        file = filedialog.asksaveasfilename(defaultextension=".json")
        if file:
            with open(file, "w", encoding="utf-8") as f:
                json.dump(self.books, f, ensure_ascii=False, indent=4)

    def load_json(self):
        file = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file:
            with open(file, "r", encoding="utf-8") as f:
                self.books = json.load(f)
            self.update_table(self.books)


if __name__ == "__main__":
    root = tk.Tk()
    app = BookTracker(root)
    root.mainloop()
