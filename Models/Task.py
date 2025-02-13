class Task:
    def __init__(
        self,
        id,
        title,
        description,
        completed=False,
        assigned_user_id=None,
    ):
        self.id = id
        self.title = title
        self.description = description
        self.completed = completed
        self.assigned_user_id = assigned_user_id
