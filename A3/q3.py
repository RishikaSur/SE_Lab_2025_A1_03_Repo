import sqlite3
from datetime import datetime

DATABASE_FILE = 'tasks.db'

def initialize_db():
    conn = sqlite3.connect(DATABASE_FILE)
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            column_name TEXT,
            description TEXT NOT NULL,
            completed BOOLEAN NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS task_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_id INTEGER,
            name TEXT,
            description TEXT,
            column_name TEXT,
            completed BOOLEAN,
            changed_at TEXT,
            change_type TEXT,
            FOREIGN KEY (task_id) REFERENCES tasks(id)
        )
    ''')

    conn.commit()
    conn.close()

initialize_db()

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

    c.execute('SELECT name, description, column_name, completed FROM tasks WHERE id = ?', (task_id,))
    old_task = c.fetchone()

    if not old_task:
        print("Task not found.")
        return

    change_type = 'edit'
    c.execute('''
        INSERT INTO task_history (task_id, name, description, column_name, completed, changed_at, change_type)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (task_id, old_task[0], old_task[1], old_task[2], old_task[3], updated_at, change_type))

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

    c.execute('SELECT name, description, column_name, completed FROM tasks WHERE id = ?', (task_id,))
    old_task = c.fetchone()

    if not old_task:
        print("Task not found.")
        return

    change_type = 'complete'
    c.execute('''
        INSERT INTO task_history (task_id, name, description, column_name, completed, changed_at, change_type)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (task_id, old_task[0], old_task[1], old_task[2], old_task[3], updated_at, change_type))

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
    c.execute('DELETE FROM task_history WHERE task_id = ?', (task_id,))
    c.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()

def show_tasks():
    conn = connect_db()
    c = conn.cursor()
    c.execute('SELECT * FROM tasks')
    tasks = c.fetchall()
    conn.close()

    print("\nTasks:")
    print("=" * 80)
    print(f"{'ID':<5} {'Task Name':<20} {'Column Name':<15} {'Description':<25} {'Status':<10} {'Created At':<20} {'Updated At'}")
    print("=" * 80)
    
    for task in tasks:
        if len(task) < 7:  # Prevent IndexError
            print(f"Skipping invalid task record: {task}")
            continue
        
        status = "Completed" if task[4] else "Pending"
        print(f"{task[0]:<5} {task[1]:<20} {task[2] or 'N/A':<15} {task[3]:<25} {status:<10} {task[5]:<20} {task[6]}")

def main():
    while True:
        print("\nTask Management CLI")
        print("Available commands: add <name> <column_name> <description>, edit <task_id> <new_name> <new_column_name> <new_description>, complete <task_id>, delete <task_id>, show, exit")
        command = input("Enter a command: ").strip().lower()

        parts = command.split(" ", 4)
        action = parts[0]

        if action == "exit":
            break
        elif action == "add" and len(parts) > 3:
            add_task(parts[1], parts[2], parts[3])
        elif action == "edit" and len(parts) > 4:
            edit_task(int(parts[1]), parts[2], parts[3], parts[4])
        elif action == "complete" and len(parts) > 1:
            complete_task(int(parts[1]))
        elif action == "delete" and len(parts) > 1:
            delete_task(int(parts[1]))
        elif action == "show":
            show_tasks()
        else:
            print("Invalid command or missing arguments. Please try again.")

if __name__ == "__main__":
    main()



