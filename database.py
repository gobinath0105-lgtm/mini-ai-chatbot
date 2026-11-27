
import sqlite3
from datetime import datetime

DB_NAME = "chatbot.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def initialize_database():

    with get_connection() as conn:

        conn.executescript("""
        CREATE TABLE IF NOT EXISTS visitors (
            visitor_id TEXT PRIMARY KEY,
            first_seen TEXT
        );

        CREATE TABLE IF NOT EXISTS conversations (
            chat_id TEXT PRIMARY KEY,
            visitor_id TEXT,
            title TEXT,
            created_at TEXT,
            FOREIGN KEY(visitor_id) REFERENCES visitors(visitor_id)
        );

        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message_id TEXT UNIQUE,
            chat_id TEXT,
            role TEXT,
            content TEXT,
            created_at TEXT,
            FOREIGN KEY(chat_id) REFERENCES conversations(chat_id)
        );

        CREATE TABLE IF NOT EXISTS feedback (
            message_id TEXT PRIMARY KEY,
            chat_id TEXT,
            rating TEXT,
            created_at TEXT,
            FOREIGN KEY(chat_id) REFERENCES conversations(chat_id)
        );
        """)


def register_visitor(visitor_id):

    with get_connection() as conn:

        conn.execute(
            "INSERT OR IGNORE INTO visitors VALUES (?, ?)",
            (visitor_id, datetime.now().isoformat())
        )


def create_conversation(chat_id, visitor_id, title):

    with get_connection() as conn:

        conn.execute(
            """INSERT INTO conversations
            VALUES (?, ?, ?, ?)""",
            (
                chat_id,
                visitor_id,
                title,
                datetime.now().isoformat()
            )
        )


def update_title(chat_id, title):

    with get_connection() as conn:

        conn.execute(
            "UPDATE conversations SET title=? WHERE chat_id=?",
            (title, chat_id)
        )


def save_message(message_id, chat_id, role, content):

    with get_connection() as conn:

        conn.execute(
            """INSERT OR IGNORE INTO messages
            (message_id, chat_id, role, content, created_at)
            VALUES (?, ?, ?, ?, ?)""",
            (
                message_id,
                chat_id,
                role,
                content,
                datetime.now().isoformat()
            )
        )


def save_feedback(message_id, chat_id, rating):

    with get_connection() as conn:

        conn.execute(
            """INSERT INTO feedback
            (message_id, chat_id, rating, created_at)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(message_id)
            DO UPDATE SET rating=excluded.rating,
                          created_at=excluded.created_at""",
            (
                message_id,
                chat_id,
                rating,
                datetime.now().isoformat()
            )
        )


def get_analytics():

    with get_connection() as conn:

        visitors = conn.execute(
            "SELECT COUNT(*) FROM visitors"
        ).fetchone()[0]

        questions = conn.execute(
            "SELECT COUNT(*) FROM messages WHERE role='user'"
        ).fetchone()[0]

        conversations = conn.execute(
            "SELECT COUNT(*) FROM conversations"
        ).fetchone()[0]

        positive = conn.execute(
            "SELECT COUNT(*) FROM feedback WHERE rating='positive'"
        ).fetchone()[0]

        negative = conn.execute(
            "SELECT COUNT(*) FROM feedback WHERE rating='negative'"
        ).fetchone()[0]

    return visitors, questions, conversations, positive, negative


def get_all_conversations():

    with get_connection() as conn:

        return conn.execute("""
            SELECT chat_id, visitor_id, title, created_at
            FROM conversations
            ORDER BY created_at DESC
        """).fetchall()


def get_conversation_messages(chat_id):

    with get_connection() as conn:

        return conn.execute("""
            SELECT role, content, created_at
            FROM messages
            WHERE chat_id=?
            ORDER BY id
        """, (chat_id,)).fetchall()


def get_popular_questions():

    with get_connection() as conn:

        return conn.execute("""
            SELECT content, COUNT(*) AS total
            FROM messages
            WHERE role='user'
            GROUP BY content
            ORDER BY total DESC
            LIMIT 10
        """).fetchall()
