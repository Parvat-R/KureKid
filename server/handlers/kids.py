import sqlite3
from .models import Kid

DB_NAME = "questions.db"

class KidHandler:
    def __init__(self, kid: Kid):
        self.kid = kid
        self.conn = None

    def _connect(self, db_name=DB_NAME) -> sqlite3.Connection:
        return sqlite3.connect(db_name)

    @staticmethod
    def _create_table():
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS kids (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                parent_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                dob DATE NOT NULL,
                FOREIGN KEY (parent_id) REFERENCES parents(id)
            )
        ''')
        conn.commit()
        conn.close()
        return True

    def create(self) -> bool:
        try:
            conn = self.conn if self.conn else self._connect()
            c = conn.cursor()
            c.execute("INSERT INTO kids (parent_id, name, dob) VALUES (?, ?, ?)",
                      (self.kid.parent_id, self.kid.name, self.kid.dob.isoformat()))
            conn.commit()
            self.kid.id = c.lastrowid
            if not self.conn:
                conn.close()
            return True
        except sqlite3.Error as e:
            print(f"Error inserting kid: {e}")
            return False

    @staticmethod
    def get(kid_id: int):
        conn = sqlite3.connect(DB_NAME)
        res = conn.execute("SELECT * FROM kids WHERE id = ?", (kid_id,))
        result = res.fetchone()
        conn.close()
        return result

    @staticmethod
    def get_by_parent(parent_id: int):
        conn = sqlite3.connect(DB_NAME)
        res = conn.execute("SELECT * FROM kids WHERE parent_id = ?", (parent_id,))
        result = res.fetchall()
        conn.close()
        return result

    def update(self) -> bool:
        try:
            conn = self.conn if self.conn else self._connect()
            c = conn.cursor()
            c.execute("UPDATE kids SET parent_id = ?, name = ?, dob = ? WHERE id = ?",
                      (self.kid.parent_id, self.kid.name, self.kid.dob.isoformat(), self.kid.id))
            conn.commit()
            if not self.conn:
                conn.close()
            return True
        except sqlite3.Error as e:
            print(f"Error updating kid: {e}")
            return False

    def delete(self) -> bool:
        try:
            conn = self.conn if self.conn else self._connect()
            c = conn.cursor()
            c.execute("DELETE FROM kids WHERE id = ?", (self.kid.id,))
            conn.commit()
            if not self.conn:
                conn.close()
            return True
        except sqlite3.Error as e:
            print(f"Error deleting kid: {e}")
            return False
