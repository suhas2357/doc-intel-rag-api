import sqlite3
from datetime import datetime
from typing import List, Optional

from app.core.config import settings
from app.core.database import get_connection


class DocumentRegistryService:
    def __init__(self):
        self._create_table()

    def _create_table(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_name TEXT NOT NULL,
                file_type TEXT,
                file_path TEXT NOT NULL,
                sha256 TEXT NOT NULL UNIQUE,
                chunk_count INTEGER NOT NULL,
                created_at TEXT NOT NULL
            )
        """)

        conn.commit()
        conn.close()

    def create_document(
        self,
        file_name: str,
        file_type: str,
        file_path: str,
        sha256: str,
        chunk_count: int
    ) -> int:
        conn = get_connection()
        cursor = conn.cursor()

        created_at = datetime.utcnow().isoformat()

        cursor.execute("""
            INSERT INTO documents (file_name, file_type, file_path, sha256, chunk_count, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (file_name, file_type, file_path, sha256, chunk_count, created_at))

        conn.commit()
        document_id = cursor.lastrowid
        conn.close()

        return document_id

    def list_documents(self) -> List[dict]:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, file_name, file_type, file_path, sha256, chunk_count, created_at
            FROM documents
            ORDER BY id DESC
        """)
        rows = cursor.fetchall()
        conn.close()

        documents = []
        for row in rows:
            documents.append({
                "id": row[0],
                "file_name": row[1],
                "file_type": row[2],
                "file_path": row[3],
                "sha256": row[4],
                "chunk_count": row[5],
                "created_at": row[6],
            })
        return documents

    def get_document_by_id(self, document_id: int) -> Optional[dict]:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, file_name, file_type, file_path, sha256, chunk_count, created_at
            FROM documents
            WHERE id = ?
        """, (document_id,))
        row = cursor.fetchone()
        conn.close()

        if not row:
            return None

        return {
            "id": row[0],
            "file_name": row[1],
            "file_type": row[2],
            "file_path": row[3],
            "sha256": row[4],
            "chunk_count": row[5],
            "created_at": row[6],
        }

    def get_by_sha256(self, sha256: str) -> Optional[dict]:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, file_name, file_type, file_path, sha256, chunk_count, created_at
            FROM documents
            WHERE sha256 = ?
        """, (sha256,))
        row = cursor.fetchone()
        conn.close()

        if not row:
            return None

        return {
            "id": row[0],
            "file_name": row[1],
            "file_type": row[2],
            "file_path": row[3],
            "sha256": row[4],
            "chunk_count": row[5],
            "created_at": row[6],
        }

    def delete_document(self, document_id: int) -> None:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM documents WHERE id = ?", (document_id,))
        conn.commit()
        conn.close()