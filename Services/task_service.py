from database.database import get_db_connection
from Models.Task import Task


class Task_Service:
    def create_task(
        self,
        id,
        title,
        description,
        assigned_user_id=None,
    ):
        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if task ID already exists
        cursor.execute("SELECT id FROM tasks WHERE id = ?", (id,))
        existing_task = cursor.fetchone()

        if existing_task:
            conn.close()
            raise ValueError(
                f"Task with ID {id} already exists! Please use a different ID."
            )

        # Insert new task if ID is unique
        cursor.execute(
            "INSERT INTO tasks (id, title, description, completed, assigned_user_id) VALUES (?, ?, ?, ?, ?)",
            (id, title, description, 0, assigned_user_id),
        )
        conn.commit()
        conn.close()
        return Task(id, title, description, assigned_user_id=assigned_user_id)

    def assign_task(
        self,
        task_id,
        user_id,
    ):
        conn = get_db_connection()
        cursor = conn.cursor()

        # Ensure the user exists before assigning
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()
        if not user:
            print("Error: User does not exist!")
            conn.close()
            return None

        cursor.execute(
            "UPDATE tasks SET assigned_user_id = ? WHERE id = ?", (user_id, task_id)
        )
        conn.commit()
        conn.close()
        print(f"Task {task_id} assigned to User {user_id}.")

    def complete_task(self, task_id):
        """Complete a specific task by its ID."""
        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if the task exists and is not already completed
        cursor.execute("SELECT * FROM tasks WHERE id = ? AND completed = 0", (task_id,))
        task_data = cursor.fetchone()

        if task_data:
            cursor.execute("UPDATE tasks SET completed = 1 WHERE id = ?", (task_id,))
            conn.commit()
            conn.close()
            return Task(
                task_data["id"],
                task_data["title"],
                task_data["description"],
            )
        else:
            conn.close()
            return None

    def get_pending_tasks(self):
        """Fetch all pending (not completed) tasks."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks WHERE completed = 0")
        tasks = [
            Task(
                row["id"],
                row["title"],
                row["description"],
            )
            for row in cursor.fetchall()
        ]
        conn.close()
        return tasks

    def get_task_history(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks WHERE completed = 1")
        tasks = [
            Task(
                row["id"],
                row["title"],
                row["description"],
                completed=True,
                assigned_user_id=row["assigned_user_id"],
            )
            for row in cursor.fetchall()
        ]
        conn.close()
        return tasks

    def get_next_task_id(self):
        """Fetch the highest task ID and return the next available ID."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(id) FROM tasks")
        max_id = cursor.fetchone()[0]
        conn.close()
        return (max_id + 1) if max_id else 1

    def delete_task(self, task_id):
        """Delete a task from the database by its ID."""
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
        conn.close()

        print(f"Task {task_id} deleted successfully.")
