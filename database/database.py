import os
import sqlite3

# Define database folder and path
DB_FOLDER = "database"
DB_NAME = os.path.join(DB_FOLDER, "database.db")

# Ensure the database directory exists
if not os.path.exists(DB_FOLDER):
    os.makedirs(DB_FOLDER)


def get_db_connection():
    """Establish a connection to the SQLite database."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_db():
    """Creates tables if they do not exist."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create Users Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL
        )
    """)

    # Create Tasks Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            completed BOOLEAN DEFAULT 0,
            assigned_user_id INTEGER,
            FOREIGN KEY (assigned_user_id) REFERENCES users(id) ON DELETE SET NULL
        )
    """)

    conn.commit()
    conn.close()


initialize_db()
