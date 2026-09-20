import sqlite3
import os
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

DB_PATH = os.getenv("DB_PATH", "users.db")


def get_connection():
    """Get a database connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize the SQLite database schema."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                first_name TEXT,
                last_name TEXT,
                username TEXT,
                links_count INTEGER DEFAULT 0,
                is_blocked INTEGER DEFAULT 0,
                joined_at TEXT
            )
            """
        )
        conn.commit()
        logger.info("Database initialized successfully at %s", DB_PATH)


def register_or_update_user(user_id: int, first_name: str, last_name: str = "", username: str = ""):
    """Register a new user or update their profile info."""
    now_str = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT user_id, links_count FROM users WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()

        if row is None:
            cursor.execute(
                """
                INSERT INTO users (user_id, first_name, last_name, username, links_count, is_blocked, joined_at)
                VALUES (?, ?, ?, ?, 0, 0, ?)
                """,
                (user_id, first_name or "", last_name or "", username or "", now_str),
            )
        else:
            cursor.execute(
                """
                UPDATE users
                SET first_name = ?, last_name = ?, username = ?, is_blocked = 0
                WHERE user_id = ?
                """,
                (first_name or "", last_name or "", username or "", user_id),
            )
        conn.commit()


def increment_user_links(user_id: int):
    """Increment the total links sent counter for a user."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET links_count = links_count + 1, is_blocked = 0 WHERE user_id = ?",
            (user_id,),
        )
        conn.commit()


def mark_user_blocked(user_id: int):
    """Mark a user as having blocked the bot."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET is_blocked = 1 WHERE user_id = ?", (user_id,))
        conn.commit()


def get_users_stats() -> dict:
    """Get overall user statistics."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) as total FROM users")
        total_users = cursor.fetchone()["total"]

        cursor.execute("SELECT COUNT(*) as blocked FROM users WHERE is_blocked = 1")
        blocked_users = cursor.fetchone()["blocked"]

        cursor.execute("SELECT SUM(links_count) as total_links FROM users")
        res = cursor.fetchone()["total_links"]
        total_links = res if res else 0

        active_users = total_users - blocked_users

        return {
            "total_users": total_users,
            "active_users": active_users,
            "blocked_users": blocked_users,
            "total_links": total_links,
        }


def get_all_users() -> list[dict]:
    """Retrieve all users sorted by links_count descending."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT user_id, first_name, last_name, username, links_count, is_blocked, joined_at
            FROM users
            ORDER BY links_count DESC, joined_at DESC
            """
        )
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
