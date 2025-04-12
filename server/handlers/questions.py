import sqlite3
from .models import Question

DB_NAME = "questions.db"

class QuestionHandler:
    def __init__(self, question: Question):
        self.question = question
        self.conn = None

    def _connect(self, db_name=DB_NAME) -> sqlite3.Connection:
        return sqlite3.connect(db_name)

    @staticmethod
    def _create_table():
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                category INTEGER NOT NULL,
                FOREIGN KEY (category) REFERENCES categories(id)
            )
        ''')
        conn.commit()
        conn.close()
        return True

    def create(self) -> bool:
        try:
            conn = self.conn if self.conn else self._connect()
            c = conn.cursor()
            c.execute("INSERT INTO questions (title, description, category) VALUES (?, ?, ?)",
                      (self.question.title, self.question.description, self.question.category))
            conn.commit()
            self.question.id = c.lastrowid
            if not self.conn:
                conn.close()
            return True
        except sqlite3.Error as e:
            print(f"Error inserting question: {e}")
            return False

    @staticmethod
    def get(question_id: int):
        conn = sqlite3.connect(DB_NAME)
        res = conn.execute("SELECT * FROM questions WHERE id = ?", (question_id,))
        result = res.fetchone()
        conn.close()
        return result

    @staticmethod
    def get_all():
        conn = sqlite3.connect(DB_NAME)
        res = conn.execute("SELECT * FROM questions")
        result = res.fetchall()
        conn.close()
        return result

    def update(self) -> bool:
        try:
            conn = self.conn if self.conn else self._connect()
            c = conn.cursor()
            c.execute("UPDATE questions SET title = ?, description = ?, category = ? WHERE id = ?",
                      (self.question.title, self.question.description, self.question.category, self.question.id))
            conn.commit()
            if not self.conn:
                conn.close()
            return True
        except sqlite3.Error as e:
            print(f"Error updating question: {e}")
            return False

    def delete(self) -> bool:
        try:
            conn = self.conn if self.conn else self._connect()
            c = conn.cursor()
            c.execute("DELETE FROM questions WHERE id = ?", (self.question.id,))
            conn.commit()
            if not self.conn:
                conn.close()
            return True
        except sqlite3.Error as e:
            print(f"Error deleting question: {e}")
            return False
