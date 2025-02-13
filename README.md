# Task Management System

## Overview
This project implements a simple **Task Management System** using Python with **SQLite for data storage** and a **Streamlit UI (Upcoming Feature)**. It allows users to:

- **Manage Tasks**: Create, assign, and complete tasks.
- **Manage Users**: Add users and retrieve user details.
- **Track Task History**: Keep a record of completed tasks.
- **Persistent Storage**: Uses SQLite to store tasks and users permanently.
- **Upcoming**: A web-based UI using **Streamlit**.

---

## Project Structure
```
TaskManagementSystem/
│── Models/
│   │── Queue.py          # Implements a queue
│   │── Stack.py          # Implements a stack
│   │── Task.py           # Task data model
│   │── User.py           # User data model
│
│── Services/
│   │── task_service.py   # Manages task-related operations
│   │── user_service.py   # Manages user-related operations
│
│── database/
│   │── database.py       # SQLite database setup and connection
│   │── database.db       # SQLite database file
│
│── main.py               # Entry point of the system
│── README.md             # Project documentation
```

---

## Installation
Ensure you have **Python 3.x** installed. Clone the repository or download the source files into a working directory.

### Install Required Dependencies
```bash
pip install sqlite3 streamlit
```

### Initialize the Database
The system uses **SQLite** for persistent storage. Run the following command to initialize the database:
```bash
python database/database.py
```

---

## Usage
### Run the Task Management System (CLI)
To start the system using the command line interface (CLI):
```bash
python main.py
```

### Features
#### 1. **User Management**
- **Add a User**:
  ```python
  User_Service.add_user(id, name, email)
  ```
- **Retrieve User Details**:
  ```python
  user = User_Service.get_users(id)
  ```

#### 2. **Task Management**
- **Create a Task**:
  ```python
  Task_Service.create_task(id, title, description)
  ```
- **Assign a Task to a User**:
  ```python
  Task_Service.assign_task(task_id, user_id)
  ```
- **Complete a Task**:
  ```python
  Task_Service.complete_task()
  ```
- **View Completed Task History**:
  ```python
  Task_Service.get_task_history()
  ```

#### 3. **Database Operations** (For Advanced Users)
You can view stored tasks and users directly in the **SQLite database**:
```bash
sqlite3 database/database.db
sqlite> SELECT * FROM tasks;
sqlite> SELECT * FROM users;
```