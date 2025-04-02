import sqlite3
import os
from datetime import datetime
from tabulate import tabulate  # For tabular output

DATABASE_FILE = 'tasks.db'

# Ensure the database exists and set up the tables if not already present
def initialize_db():
    conn = sqlite3.connect(DATABASE_FILE)
    c = conn.cursor()

    # Create tasks table if not exists (add a new column 'column_name')
    c.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,  -- Column for task name
            column_name TEXT,  -- New column for column_name
            description TEXT NOT NULL,
            completed BOOLEAN NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    ''')

    # Create task history table if not exists
    c.execute('''
        CREATE TABLE IF NOT EXISTS task_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_id INTEGER,
            name TEXT,
            description TEXT,
            column_name TEXT,  -- Add column_name in history
            completed BOOLEAN,
            changed_at TEXT,
            change_type TEXT,
            FOREIGN KEY (task_id) REFERENCES tasks(id)
        )
    ''')

    conn.commit()
    conn.close()

initialize_db()  # Call to initialize tables when the program starts

def connect_db():
    return sqlite3.connect(DATABASE_FILE)

def add_task(name, column_name, description):
    conn = connect_db()
    c = conn.cursor()
    created_at = updated_at = datetime.now().isoformat()
    c.execute('''
        INSERT INTO tasks (name, column_name, description, completed, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (name, column_name, description, False, created_at, updated_at))
    conn.commit()
    conn.close()

def edit_task(task_id, new_name, new_column_name, new_description):
    conn = connect_db()
    c = conn.cursor()
    updated_at = datetime.now().isoformat()

    # Get the old task details to log the history
    c.execute('SELECT name, description, column_name, completed FROM tasks WHERE id = ?', (task_id,))
    old_task = c.fetchone()

    # Log the change to task history
    change_type = 'edit'
    c.execute('''
        INSERT INTO task_history (task_id, name, description, column_name, completed, changed_at, change_type)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (task_id, old_task[0], old_task[1], old_task[2], old_task[3], updated_at, change_type))

    # Update the task's name, column_name, and description
    c.execute('''
        UPDATE tasks
        SET name = ?, column_name = ?, description = ?, updated_at = ?
        WHERE id = ?
    ''', (new_name, new_column_name, new_description, updated_at, task_id))

    conn.commit()
    conn.close()

def complete_task(task_id):
    conn = connect_db()
    c = conn.cursor()
    updated_at = datetime.now().isoformat()

    # Get the old task details to log the history
    c.execute('SELECT name, description, column_name, completed FROM tasks WHERE id = ?', (task_id,))
    old_task = c.fetchone()

    # Log the change to task history
    change_type = 'complete'
    c.execute('''
        INSERT INTO task_history (task_id, name, description, column_name, completed, changed_at, change_type)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (task_id, old_task[0], old_task[1], old_task[2], old_task[3], updated_at, change_type))

    # Mark the task as completed
    c.execute('''
        UPDATE tasks
        SET completed = ?, updated_at = ?
        WHERE id = ?
    ''', (True, updated_at, task_id))

    conn.commit()
    conn.close()

def delete_task(task_id):
    conn = connect_db()
    c = conn.cursor()

    # Check if task_history table exists before deleting entries
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='task_history'")
    table_exists = c.fetchone()

    if table_exists:
        # First, delete the task from the history table
        c.execute('DELETE FROM task_history WHERE task_id = ?', (task_id,))
    else:
        print("task_history table does not exist.")

    # Now delete the task itself from the tasks table
    c.execute('DELETE FROM tasks WHERE id = ?', (task_id,))

    conn.commit()
    conn.close()

def show_tasks():
    conn = connect_db()
    c = conn.cursor()
    c.execute('SELECT * FROM tasks')
    tasks = c.fetchall()
    conn.close()

    table_data = []
    for task in tasks:
        status = "Completed" if task[4] else "Pending"
        table_data.append([task[0], task[1], task[2], task[3], status, task[5], task[6]])

    headers = ["ID", "Task Name", "Column Name", "Description", "Status", "Created At", "Updated At"]
    print(tabulate(table_data, headers, tablefmt="grid"))

def show_task_history(task_id):
    conn = connect_db()
    c = conn.cursor()
    c.execute('SELECT * FROM task_history WHERE task_id = ?', (task_id,))
    history = c.fetchall()
    conn.close()

    table_data = []
    for record in history:
        change_type = record[7]
        table_data.append([record[0], record[2], record[3], record[4], "Completed" if record[5] else "Pending", record[6], change_type])

    headers = ["History ID", "Task Name", "Description", "Column Name", "Status", "Changed At", "Change Type"]
    print(tabulate(table_data, headers, tablefmt="grid"))

# Switch-case simulation
def switch_case(command, *args):
    switch_dict = {
        "add": add_task,
        "edit": edit_task,
        "complete": complete_task,
        "delete": delete_task,
        "show": show_tasks,
        "history": show_task_history,
    }

    # Get the function from the dictionary and execute it
    func = switch_dict.get(command)
    if func:
        func(*args)  # Call the function with arguments
    else:
        print(f"Invalid command: {command}")

# Main CLI loop
def main():
    while True:
        print("\nTask Management CLI")
        print("Available commands: add <name> <column_name> <description>, edit <task_id> <new_name> <new_column_name> <new_description>, complete <task_id>, delete <task_id>, show, history <task_id>, exit")
        command = input("Enter a command: ").strip().lower()

        if command == "exit":
            break

        # Split the command to get the main action and arguments
        parts = command.split(" ", 4)
        action = parts[0]

        if action == "add" and len(parts) > 3:
            name = parts[1]
            column_name = parts[2]
            description = parts[3]
            switch_case(action, name, column_name, description)

        elif action == "edit" and len(parts) > 4:
            task_id = int(parts[1])
            new_name = parts[2]
            new_column_name = parts[3]
            new_description = parts[4]
            switch_case(action, task_id, new_name, new_column_name, new_description)

        elif action == "complete" and len(parts) > 1:
            task_id = int(parts[1])
            switch_case(action, task_id)

        elif action == "delete" and len(parts) > 1:
            task_id = int(parts[1])
            switch_case(action, task_id)

        elif action == "show":
            switch_case(action)

        elif action == "history" and len(parts) > 1:
            task_id = int(parts[1])
            switch_case(action, task_id)

        else:
            print("Invalid command or missing arguments. Please try again.")

if __name__ == "__main__":
    main()



