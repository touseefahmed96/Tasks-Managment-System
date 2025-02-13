from Models.Queue import Queue
from Models.Stack import Stack
from Models.Task import Task


class Task_Service:
    def __init__(self):
        self.tasks = []
        self.task_queue = Queue()
        self.task_history = Stack()

    def create_task(self, id, title, description):
        task = Task(id, title, description)
        self.tasks.append(task)
        self.task_queue(task)
        return task

    def complete_task(self):
        if not self.task_queue.is_empty():
            task = self.task_queue.dequeue()
            self.task_history.push(task)
            return task
        return None

    def get_task_history(self):
        return self.task_history
