import sqlite3
from .models import Category

DB_NAME = "questions.db"

class CategoryHandler:
    def __init__(self, category: Category):
        self.category = category
        self.conn = None

    def _connect(self, db_name=DB_NAME) -> sqlite3.Connection:
        return sqlite3.connect(db_name)

    @staticmethod
    def _create_table():
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()
        return True

    def create(self) -> bool:
        try:
            conn = self.conn if self.conn else self._connect()
            c = conn.cursor()
            c.execute("INSERT INTO categories (text) VALUES (?)", (self.category.text,))
            conn.commit()
            self.category.id = c.lastrowid
            if not self.conn:
                conn.close()
            return True
        except sqlite3.Error as e:
            print(f"Error inserting category: {e}")
            return False

    @staticmethod
    def get(category_id: int):
        conn = sqlite3.connect(DB_NAME)
        res = conn.execute("SELECT * FROM categories WHERE id = ?", (category_id,))
        result = res.fetchone()
        conn.close()
        return result

    @staticmethod
    def get_all():
        conn = sqlite3.connect(DB_NAME)
        res = conn.execute("SELECT * FROM categories")
        result = res.fetchall()
        conn.close()
        return result

    def update(self) -> bool:
        try:
            conn = self.conn if self.conn else self._connect()
            c = conn.cursor()
            c.execute("UPDATE categories SET text = ? WHERE id = ?",
                      (self.category.text, self.category.id))
            conn.commit()
            if not self.conn:
                conn.close()
            return True
        except sqlite3.Error as e:
            print(f"Error updating category: {e}")
            return False

    def delete(self) -> bool:
        try:
            conn = self.conn if self.conn else self._connect()
            c = conn.cursor()
            c.execute("DELETE FROM categories WHERE id = ?", (self.category.id,))
            conn.commit()
            if not self.conn:
                conn.close()
            return True
        except sqlite3.Error as e:
            print(f"Error deleting category: {e}")
            return False
