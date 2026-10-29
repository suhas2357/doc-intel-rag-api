import sqlite3
from app.core.config import settings


def get_connection():
    """
    Return SQLite connection.
    row_factory is set so rows behave like dict-style objects.
    """
    conn = sqlite3.connect(settings.SQLITE_DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """
    Create required tables if they do not exist.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_name TEXT NOT NULL,
            file_type TEXT,
            file_path TEXT NOT NULL,
            sha256 TEXT NOT NULL UNIQUE,
            chunk_count INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()