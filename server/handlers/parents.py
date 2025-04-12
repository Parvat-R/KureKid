import sqlite3
from .models import Parent

DB_NAME = "questions.db"

class ParentHandler:
    def __init__(self, parent: Parent):
        self.parent = parent
        self.conn = None

    def _connect(self, db_name=DB_NAME) -> sqlite3.Connection:
        return sqlite3.connect(db_name)

    @staticmethod
    def _create_table():
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS parents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()
        return True

    def create(self) -> bool:
        try:
            conn = self.conn if self.conn else self._connect()
            c = conn.cursor()
            c.execute("INSERT INTO parents (name, email, password) VALUES (?, ?, ?)",
                      (self.parent.name, self.parent.email, self.parent.password))
            conn.commit()
            self.parent.id = c.lastrowid
            if not self.conn:
                conn.close()
            return True
        except sqlite3.Error as e:
            print(f"Error inserting parent: {e}")
            return False

    @staticmethod
    def get(parent_id: int):
        conn = sqlite3.connect(DB_NAME)
        res = conn.execute("SELECT * FROM parents WHERE id = ?", (parent_id,))
        result = res.fetchone()
        conn.close()
        return result

    @staticmethod
    def get_all():
        conn = sqlite3.connect(DB_NAME)
        res = conn.execute("SELECT * FROM parents")
        result = res.fetchall()
        conn.close()
        return result

    def update(self) -> bool:
        try:
            conn = self.conn if self.conn else self._connect()
            c = conn.cursor()
            c.execute("UPDATE parents SET name = ?, email = ?, password = ? WHERE id = ?",
                      (self.parent.name, self.parent.email, self.parent.password, self.parent.id))
            conn.commit()
            if not self.conn:
                conn.close()
            return True
        except sqlite3.Error as e:
            print(f"Error updating parent: {e}")
            return False

    def delete(self) -> bool:
        try:
            conn = self.conn if self.conn else self._connect()
            c = conn.cursor()
            c.execute("DELETE FROM parents WHERE id = ?", (self.parent.id,))
            conn.commit()
            if not self.conn:
                conn.close()
            return True
        except sqlite3.Error as e:
            print(f"Error deleting parent: {e}")
            return False
