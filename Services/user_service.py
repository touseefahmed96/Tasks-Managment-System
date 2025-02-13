import sqlite3

from database.database import get_db_connection
from Models.User import User


class User_Service:
    def add_user(self, id, name, email):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (id, name, email) VALUES (?, ?, ?)",
                (id, name, email),
            )
            conn.commit()
            return User(name, id, email)
        except sqlite3.IntegrityError:
            print("User with this ID already exists!")
        finally:
            conn.close()

    def get_users(self, id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (id,))
        user_data = cursor.fetchone()
        conn.close()
        return (
            User(user_data["name"], user_data["id"], user_data["email"])
            if user_data
            else None
        )
