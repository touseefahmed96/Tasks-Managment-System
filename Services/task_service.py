from database.database import get_db_connection
from Models.Task import Task


class Task_Service:
    def create_task(self, id, title, description):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO tasks (id, title, description, completed) VALUES (?, ?, ?, ?)",
            (id, title, description, 0),
        )
        conn.commit()
        conn.close()
        return Task(id, title, description)

    def complete_task(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM tasks WHERE completed = 0 ORDER BY id ASC LIMIT 1"
        )
        task_data = cursor.fetchone()
        if task_data:
            task = Task(task_data["id"], task_data["title"], task_data["description"])
            cursor.execute("UPDATE tasks SET completed = 1 WHERE id = ?", (task.id,))
            conn.commit()
        else:
            task = None
        conn.close()
        return task

    def get_task_history(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks WHERE completed = 1")
        tasks = [
            Task(row["id"], row["title"], row["description"])
            for row in cursor.fetchall()
        ]
        conn.close()
        return tasks
