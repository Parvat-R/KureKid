import sqlite3
from .models import KidToQuestionScore

DB_NAME = "questions.db"

class KidToQuestionScoreHandler:
    def __init__(self, score_entry: KidToQuestionScore):
        self.score_entry = score_entry
        self.conn = None

    def _connect(self, db_name=DB_NAME) -> sqlite3.Connection:
        return sqlite3.connect(db_name)

    @staticmethod
    def _create_table():
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS kid_to_question_score (
                entry_id INTEGER PRIMARY KEY AUTOINCREMENT,
                kid_id INTEGER NOT NULL,
                question_id INTEGER NOT NULL,
                score INTEGER NOT NULL,
                FOREIGN KEY (kid_id) REFERENCES kids(id),
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
            c.execute("INSERT INTO kid_to_question_score (kid_id, question_id, score) VALUES (?, ?, ?)",
                      (self.score_entry.kid_id, self.score_entry.question_id, self.score_entry.score))
            conn.commit()
            self.score_entry.entry_id = c.lastrowid
            if not self.conn:
                conn.close()
            return True
        except sqlite3.Error as e:
            print(f"Error inserting score: {e}")
            return False

    @staticmethod
    def get(entry_id: int):
        conn = sqlite3.connect(DB_NAME)
        res = conn.execute("SELECT * FROM kid_to_question_score WHERE entry_id = ?", (entry_id,))
        result = res.fetchone()
        conn.close()
        return result

    @staticmethod
    def get_all():
        conn = sqlite3.connect(DB_NAME)
        res = conn.execute("SELECT * FROM kid_to_question_score")
        result = res.fetchall()
        conn.close()
        return result

    def update(self) -> bool:
        try:
            conn = self.conn if self.conn else self._connect()
            c = conn.cursor()
            c.execute('''UPDATE kid_to_question_score 
                         SET kid_id = ?, question_id = ?, score = ? 
                         WHERE entry_id = ?''',
                      (self.score_entry.kid_id, self.score_entry.question_id,
                       self.score_entry.score, self.score_entry.entry_id))
            conn.commit()
            if not self.conn:
                conn.close()
            return True
        except sqlite3.Error as e:
            print(f"Error updating score: {e}")
            return False

    def delete(self) -> bool:
        try:
            conn = self.conn if self.conn else self._connect()
            c = conn.cursor()
            c.execute("DELETE FROM kid_to_question_score WHERE entry_id = ?", (self.score_entry.entry_id,))
            conn.commit()
            if not self.conn:
                conn.close()
            return True
        except sqlite3.Error as e:
            print(f"Error deleting score: {e}")
            return False
