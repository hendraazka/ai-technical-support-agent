
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "conversations.db"


def initialize_database():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id INTEGER NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_conversations_chat
            ON conversations(chat_id, id)
        """)


def get_history(chat_id: int, limit: int = 10) -> list[dict[str, str]]:
    with sqlite3.connect(DB_PATH) as conn:
        rows = conn.execute("""
            SELECT role, content
            FROM conversations
            WHERE chat_id = ?
            ORDER BY id DESC
            LIMIT ?
        """, (chat_id, limit)).fetchall()

    return [
        {"role": role, "content": content}
        for role, content in reversed(rows)
    ]


def save_turn(chat_id: int, user_message: str, assistant_message: str):
    with sqlite3.connect(DB_PATH) as conn:
        conn.executemany("""
            INSERT INTO conversations (chat_id, role, content)
            VALUES (?, ?, ?)
        """, [
            (chat_id, "user", user_message),
            (chat_id, "assistant", assistant_message),
        ])


def clear_history(chat_id: int):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "DELETE FROM conversations WHERE chat_id = ?",
            (chat_id,),
        )
