import sqlite3
import hashlib
from .models import Parent, Kid

DB_NAME = "database.db"

class ParentHandler:
    def __init__(self, parent: Parent):
        self.parent: Parent = parent
        self.conn: None | sqlite3.Connection = None
    
    def _connect(self, db_name=DB_NAME) -> sqlite3.Connection:
        return sqlite3.connect(db_name)
    
    @staticmethod
    def _create_table() -> None:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS parents
                (
                    id integer PRIMARY KEY,
                    name text not null,
                    email text unique not null, 
                    password text not null
                );
        ''')
        conn.commit()
        conn.close()
        return None

    @staticmethod
    def get(_id: int):
        conn = sqlite3.connect(DB_NAME)
        conn.execute("select * from parents where id = ?", (_id,))
        result = conn.fetchone()
        conn.close()
        return result
    
    @staticmethod
    def get_by_email(email: str):
        conn = sqlite3.connect(DB_NAME)
        conn.execute("select * from parents where email = ?", (email,))
        result = conn.fetchone()
        conn.close()
        return result
    
    @staticmethod
    def match_email_password(email, password):
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("SELECT * FROM parents WHERE email = ? AND password = ?", (email, password))
        result = c.fetchone()
        conn.close()
        return True if result else False


    def create(self) -> bool:
        if self.parent is None:
            return False
        
        try:
            conn = self.conn if self.conn else self._connect()
            c = conn.cursor()
            c.execute(
                "INSERT INTO parents (name, email, password) VALUES (?, ?, ?)", 
                (self.parent.name, self.parent.email, self.parent.password)
            )
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            print(f"An error occurred: {e.args[0]}")
            return False
    

    def update(self) -> bool:
        if self.parent is None:
            return False
        
        conn = self.conn if self.conn else self._connect()
        c = conn.cursor()
        c.execute(
            "UPDATE parents SET name = ?, email = ?, password = ?WHERE id = ?", 
            (self.parent.name, self.parent.email, self.parent.password, self.parent.id)
        )
        res = c.fetchone()
        conn.commit()

        # close the connection only if the connection was made for this function
        if not self.conn:
            conn.close()
    
        return res


class KidHandler:
    def __init__(self, kid: Kid):
        self.kid = kid
        self.conn = None

    def _connect(self, db_name: str = "kids.db") -> sqlite3.Connection:
        return sqlite3.connect(db_name)
    
    @staticmethod
    def _create_table():
        conn = sqlite3.connect("kids.db")
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS kids (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                parent_id int,
                name text NOT NULL,
                dob date not null
            )
        ''')
        conn.commit()
        conn.close()
        return True
    
    def create(self):
        if self.kid is None:
            return False
        
        try:
            conn = self.conn if self.conn else self._connect()
            c = conn.cursor()
            c.execute(
                "INSERT INTO kids (parent_id, name, dob) VALUES (?, ?, ?)", (self.kid.parent_id, self.kid.name, self.kid.dob)
            )
            conn.commit()
            self.kid.id = c.lastrowid
            return True
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            return False
    
    @staticmethod
    def get(id):
        conn = sqlite3.connect("kids.db")
        res = conn.execute("SELECT * FROM kids WHERE id = ?", (id,))
        return res.fetchone()
    
    @staticmethod
    def get_kids_by_parent(self, parent_id):
        conn = sqlite3.connect("kids.db")
        res = conn.execute("SELECT * FROM kids WHERE parent_id = ?", (parent_id,))
        return res.fetchall()
