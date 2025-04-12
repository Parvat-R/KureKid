import sqlite3
from typing import List, Optional, Dict, Any
from models import KidToQuestionScore, Question, Category

DB_NAME = "questions.db"

class KidPerformanceAnalyzer:
    def __init__(self, kid_id: int):
        self.kid_id = kid_id
        self.conn = sqlite3.connect(DB_NAME)
        self.conn.row_factory = sqlite3.Row  # enables dict-like rows

    def _execute_query(self, query: str, params: tuple = ()) -> List[sqlite3.Row]:
        cur = self.conn.cursor()
        cur.execute(query, params)
        return cur.fetchall()

    def get_category_performance(self) -> List[Dict[str, Any]]:
        query = '''
        SELECT q.category, c.text AS category_text, AVG(kqs.score) AS average_score
        FROM KidToQuestionScore kqs
        JOIN Question q ON kqs.question_id = q.id
        JOIN Category c ON q.category = c.id
        WHERE kqs.kid_id = ?
        GROUP BY q.category
        ORDER BY average_score DESC
        '''
        rows = self._execute_query(query, (self.kid_id,))
        return [dict(row) for row in rows]

    def get_question_performance(self) -> List[Dict[str, Any]]:
        query = '''
        SELECT kqs.question_id, q.title, q.description, kqs.score
        FROM KidToQuestionScore kqs
        JOIN Question q ON kqs.question_id = q.id
        WHERE kqs.kid_id = ?
        ORDER BY kqs.score ASC
        '''
        rows = self._execute_query(query, (self.kid_id,))
        return [dict(row) for row in rows]

    def get_lowest_performing_category(self) -> Optional[int]:
        query = '''
        SELECT q.category
        FROM KidToQuestionScore kqs
        JOIN Question q ON kqs.question_id = q.id
        WHERE kqs.kid_id = ?
        GROUP BY q.category
        ORDER BY AVG(kqs.score) ASC
        LIMIT 1
        '''
        rows = self._execute_query(query, (self.kid_id,))
        return rows[0]['category'] if rows else None

    def suggest_next_question(self) -> Optional[Dict[str, Any]]:
        category = self.get_lowest_performing_category()
        if category is None:
            return None
        
        query = '''
        SELECT q.id, q.title, q.description
        FROM Question q
        WHERE q.category = ?
        AND q.id NOT IN (
            SELECT question_id FROM KidToQuestionScore WHERE kid_id = ?
        )
        LIMIT 1
        '''
        rows = self._execute_query(query, (category, self.kid_id))
        return dict(rows[0]) if rows else None

    def close(self):
        self.conn.close()
