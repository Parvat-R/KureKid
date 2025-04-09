import sqlite3
from .models import Option

DB_NAME = "questions.db"

class OptionHandler:
    def __init__(self, option: Option):
        self.option = option
        self.conn = None

    def _connect(self, db_name=DB_NAME) -> sqlite3.Connection:
        return sqlite3.connect(db_name)

    @staticmethod
    def _create_table():
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS options (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question_id INTEGER NOT NULL,
                text TEXT NOT NULL,
                FOREIGN KEY (question_id) REFERENCES questions(id)
            )
        ''')
        conn.commit()
        conn.close()
        return True

    def create(self) -> bool:
        try:
            conn = self.conn if self.conn else self._connect()
            c = conn.cursor()
            c.execute("INSERT INTO options (question_id, text) VALUES (?, ?)",
                      (self.option.question_id, self.option.text))
            conn.commit()
            self.option.id = c.lastrowid
            if not self.conn:
                conn.close()
            return True
        except sqlite3.Error as e:
            print(f"Error inserting option: {e}")
            return False

    @staticmethod
    def get(option_id: int):
        conn = sqlite3.connect(DB_NAME)
        res = conn.execute("SELECT * FROM options WHERE id = ?", (option_id,))
        result = res.fetchone()
        conn.close()
        return result

    @staticmethod
    def get_all():
        conn = sqlite3.connect(DB_NAME)
        res = conn.execute("SELECT * FROM options")
        result = res.fetchall()
        conn.close()
        return result

    def update(self) -> bool:
        try:
            conn = self.conn if self.conn else self._connect()
            c = conn.cursor()
            c.execute("UPDATE options SET question_id = ?, text = ? WHERE id = ?",
                      (self.option.question_id, self.option.text, self.option.id))
            conn.commit()
            if not self.conn:
                conn.close()
            return True
        except sqlite3.Error as e:
            print(f"Error updating option: {e}")
            return False

    def delete(self) -> bool:
        try:
            conn = self.conn if self.conn else self._connect()
            c = conn.cursor()
            c.execute("DELETE FROM options WHERE id = ?", (self.option.id,))
            conn.commit()
            if not self.conn:
                conn.close()
            return True
        except sqlite3.Error as e:
            print(f"Error deleting option: {e}")
            return False
