"""
Database connection manager for Jassas Search Engine.
Provides connection handling for all services.
"""
import sqlite3
import os
from contextlib import contextmanager

# Paths
DB_FOLDER = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data')
DB_PATH = os.path.join(DB_FOLDER, 'jassas.db')


def get_connection() -> sqlite3.Connection:
    """Get a database connection with optimized settings."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Access columns by name
    conn.execute("PRAGMA foreign_keys = ON")  # Enforce foreign keys
    conn.execute("PRAGMA journal_mode = WAL")  # Better concurrency
    return conn


@contextmanager
def get_db():
    """Context manager for database connections.

    Usage:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM frontier")
    """
    conn = get_connection()
    try:
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()


def db_exists() -> bool:
    """Check if database file exists."""
    return os.path.exists(DB_PATH)
