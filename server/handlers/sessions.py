import sqlite3
from .models import Session

DB_NAME = "questions.db"

class SessionHandler:
    def __init__(self, session: Session):
        self.session = session
        self.conn = None

    def _connect(self, db_name=DB_NAME) -> sqlite3.Connection:
        return sqlite3.connect(db_name)

    @staticmethod
    def _create_table():
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                session_id TEXT PRIMARY KEY,
                created_on TEXT NOT NULL,
                parent_id INTEGER NOT NULL,
                otp INTEGER NOT NULL,
                device TEXT NOT NULL,
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
            c.execute("INSERT INTO sessions (session_id, created_on, parent_id, otp, device) VALUES (?, ?, ?, ?, ?)",
                      (self.session.session_id, self.session.created_on.isoformat(),
                       self.session.parent_id, self.session.otp, self.session.device))
            conn.commit()
            if not self.conn:
                conn.close()
            return True
        except sqlite3.Error as e:
            print(f"Error inserting session: {e}")
            return False

    @staticmethod
    def get(session_id: str):
        conn = sqlite3.connect(DB_NAME)
        res = conn.execute("SELECT * FROM sessions WHERE session_id = ?", (session_id,))
        result = res.fetchone()
        conn.close()
        return result

    @staticmethod
    def get_all():
        conn = sqlite3.connect(DB_NAME)
        res = conn.execute("SELECT * FROM sessions")
        result = res.fetchall()
        conn.close()
        return result

    def update(self) -> bool:
        try:
            conn = self.conn if self.conn else self._connect()
            c = conn.cursor()
            c.execute('''
                UPDATE sessions SET created_on = ?, parent_id = ?, otp = ?, device = ? 
                WHERE session_id = ?
            ''', (self.session.created_on.isoformat(), self.session.parent_id,
                  self.session.otp, self.session.device, self.session.session_id))
            conn.commit()
            if not self.conn:
                conn.close()
            return True
        except sqlite3.Error as e:
            print(f"Error updating session: {e}")
            return False

    def delete(self) -> bool:
        try:
            conn = self.conn if self.conn else self._connect()
            c = conn.cursor()
            c.execute("DELETE FROM sessions WHERE session_id = ?", (self.session.session_id,))
            conn.commit()
            if not self.conn:
                conn.close()
            return True
        except sqlite3.Error as e:
            print(f"Error deleting session: {e}")
            return False
