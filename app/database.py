"""
Database layer — SQLite.
Handles persistence for test results and scores.
"""

import sqlite3
import os

# Default to local file, but allow override for testing/production environments
DB_PATH = os.environ.get("DB_PATH", "scores.db")

def get_connection():
    """Returns a connection to the SQLite database with Row factory enabled."""
    conn = sqlite3.connect(DB_PATH)
    # This allows accessing columns by name instead of index
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes the database schema if it doesn't exist."""
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS scores (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name  TEXT NOT NULL,
                second_name TEXT NOT NULL,
                score       INTEGER NOT NULL
            )
        """)
        conn.commit()

def insert_scores(records: list[dict]):
    with get_connection() as conn:
        for r in records:
            # Only insert if this person doesn't already exist
            existing = conn.execute(
                "SELECT id FROM scores WHERE LOWER(first_name) = LOWER(?) AND LOWER(second_name) = LOWER(?)",
                (r["First Name"], r["Second Name"])
            ).fetchone()

            if not existing:
                conn.execute(
                    "INSERT INTO scores (first_name, second_name, score) VALUES (?, ?, ?)",
                    (r["First Name"], r["Second Name"], int(r["Score"]))
                )
        conn.commit()
     

def get_top_scorers():
    with get_connection() as conn:
        row = conn.execute("SELECT MAX(score) as max_score FROM scores").fetchone()

        if row is None or row["max_score"] is None:
            return [], 0

        max_score = row["max_score"]

        rows = conn.execute(
            """
            SELECT first_name, second_name, score
            FROM   scores
            WHERE  score = ?
            ORDER  BY first_name ASC, second_name ASC
            """,
            (max_score,),
        ).fetchall()

        scorers = [
            {"full_name": f"{r['first_name']} {r['second_name']}", "score": r["score"]}
            for r in rows
        ]

    return scorers, max_score


def get_score_by_name(first_name: str, second_name: str):
    """Retrieves the most recent score for a specific person, case-insensitive."""
    with get_connection() as conn:
        row = conn.execute("""
            SELECT first_name, second_name, score
            FROM   scores
            WHERE  LOWER(first_name) = LOWER(?)
              AND  LOWER(second_name) = LOWER(?)
            ORDER  BY id DESC
            LIMIT  1
        """, (first_name.strip(), second_name.strip())).fetchone()

    if not row:
        return None

    return {"full_name": f"{row['first_name']} {row['second_name']}", "score": row['score']}

def add_score(first_name: str, second_name: str, score: int):
    """Adds a single score record to the database (used by the REST API)."""
    with get_connection() as conn:
        cursor = conn.execute(
            "INSERT INTO scores (first_name, second_name, score) VALUES (?, ?, ?)",
            (first_name.strip(), second_name.strip(), score)
        )
        conn.commit()
        new_id = cursor.lastrowid

    return {"id": new_id, "first_name": first_name, "second_name": second_name, "score": score}