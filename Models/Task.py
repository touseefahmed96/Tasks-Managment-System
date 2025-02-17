class Task:
    def __init__(
        self,
        id,
        title,
        description,
        completed=False,
        assigned_user_id=None,
        due_date=None,
        priority="Medium",
    ):
        self.id = id
        self.title = title
        self.description = description
        self.completed = completed
        self.assigned_user_id = assigned_user_id
        self.due_date = due_date
        self.priority = priority
