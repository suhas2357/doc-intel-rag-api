import os
import sqlite3

from app.core.config import settings


def get_connection():
    db_path = settings.SQLITE_DB_PATH

    db_dir = os.path.dirname(db_path)
    if db_dir:
        os.makedirs(db_dir, exist_ok=True)

    conn = sqlite3.connect(db_path)
    return conn