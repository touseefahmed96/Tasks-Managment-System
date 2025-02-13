# Task Management System

## Overview
This project implements a simple task management system using Python. It includes the following components:

- **Graph**: Represents a graph structure.
- **Queue**: Implements a queue data structure using `collections.deque`.
- **Stack**: Implements a stack data structure.
- **Task**: Represents a task with an `id`, `title`, and `description`.
- **User**: Represents a user with `name`, `id`, and `email`.
- **Task_Service**: Manages task creation, task completion, and maintains a task history.
- **User_Service**: Manages user data storage and retrieval.

## Project Structure
```
TaskManagementSystem/
│── Models/
│   │── Queue.py
│   │── Stack.py
│   │── Task.py
│   │── User.py
│
│── Services/
│   │── task_service.py
│   │── user_service.py
│
│── main.py
│── README.md
```

## Installation
Ensure you have Python installed on your system (Python 3.x recommended). Clone the repository or copy the source files into a working directory.

## Usage
To run the task management system, execute the following command:

```bash
python main.py
```

### Features
1. **User Management**:
   - Add users with `User_Service.add_user(name, id, email)`.
   - Retrieve user details with `User_Service.get_users(id)`.

2. **Task Management**:
   - Create tasks using `Task_Service.create_task(id, title, description)`.
   - Complete tasks using `Task_Service.complete_task()`.
   - Retrieve task history using `Task_Service.get_task_history()`.



