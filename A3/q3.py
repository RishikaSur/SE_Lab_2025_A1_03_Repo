import sqlite3
import sys
from datetime import datetime

# Initialize SQLite connection and alter schema if needed
def init_db():
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()

    # Alter tasks table to add missing columns
    try:
        cursor.execute('''ALTER TABLE tasks ADD COLUMN name TEXT NOT NULL''')
    except sqlite3.OperationalError:
        print("Column 'name' already exists or table structure is incompatible.")

    try:
        cursor.execute('''ALTER TABLE tasks ADD COLUMN column_name TEXT''')
    except sqlite3.OperationalError:
        print("Column 'column_name' already exists or table structure is incompatible.")
    
    # Create task_history table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS task_history (
                        history_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        task_id INTEGER,
                        name TEXT,
                        column_name TEXT,
                        description TEXT,
                        completed BOOLEAN,
                        created_at TEXT,
                        updated_at TEXT,
                        timestamp TEXT,
                        action TEXT,
                        FOREIGN KEY (task_id) REFERENCES tasks(id)
                    )''')
    conn.commit()
    conn.close()

# Add a task
def add_task(name, column_name, description):
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()

    created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    updated_at = created_at  # Initially, created_at and updated_at will be the same
    cursor.execute('''INSERT INTO tasks (name, column_name, description, created_at, updated_at) 
                      VALUES (?, ?, ?, ?, ?)''', (name, column_name, description, created_at, updated_at))

    conn.commit()
    conn.close()
    print("Task added successfully.")

# List all tasks
def list_tasks():
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()

    cursor.execute('''SELECT id, name, column_name, description, completed, created_at, updated_at FROM tasks''')
    tasks = cursor.fetchall()

    if tasks:
        for task in tasks:
            print("ID: " + str(task[0]) + " | Name: " + task[1] + " | Column: " + str(task[2]) + 
                  " | Description: " + task[3] + " | Completed: " + str(task[4]) + 
                  " | Created At: " + task[5] + " | Updated At: " + task[6])
    else:
        print("No tasks available.")
    
    conn.close()

# Edit a task description or other attributes
def edit_task(task_id, name, column_name, description):
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()

    # Get current task state for history logging
    cursor.execute('''SELECT name, column_name, description, completed, created_at, updated_at FROM tasks WHERE id = ?''', (task_id,))
    task = cursor.fetchone()

    if task:
        old_name, old_column_name, old_description, old_completed, created_at, old_updated_at = task

        # Insert into history
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute('''INSERT INTO task_history (task_id, name, column_name, description, completed, created_at, updated_at, timestamp, action) 
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                       (task_id, old_name, old_column_name, old_description, old_completed, created_at, old_updated_at, timestamp, 'edited'))

        # Update task with new values
        updated_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute('''UPDATE tasks SET name = ?, column_name = ?, description = ?, updated_at = ? WHERE id = ?''',
                       (name, column_name, description, updated_at, task_id))

        conn.commit()
        print("Task updated successfully.")
    else:
        print("Task not found.")

    conn.close()

# Mark a task as completed
def complete_task(task_id):
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()

    # Get current task state for history logging
    cursor.execute('''SELECT name, column_name, description, completed, created_at, updated_at FROM tasks WHERE id = ?''', (task_id,))
    task = cursor.fetchone()

    if task:
        old_name, old_column_name, old_description, old_completed, created_at, old_updated_at = task

        if old_completed == 1:
            print("Task already completed.")
            return

        # Insert into history
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute('''INSERT INTO task_history (task_id, name, column_name, description, completed, created_at, updated_at, timestamp, action) 
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                       (task_id, old_name, old_column_name, old_description, old_completed, created_at, old_updated_at, timestamp, 'completed'))

        # Mark task as completed
        updated_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute('''UPDATE tasks SET completed = 1, updated_at = ? WHERE id = ?''', (updated_at, task_id))
        
        conn.commit()
        print("Task marked as completed.")
    else:
        print("Task not found.")

    conn.close()

# View task history
def view_task_history(task_id):
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()

    cursor.execute('''SELECT timestamp, action, name, column_name, description, completed, created_at, updated_at 
                      FROM task_history WHERE task_id = ? ORDER BY timestamp DESC''', (task_id,))
    history = cursor.fetchall()

    if history:
        for record in history:
            print("Timestamp: " + record[0] + " | Action: " + record[1] + 
                  " | Name: " + record[2] + " | Column: " + str(record[3]) + 
                  " | Description: " + record[4] + " | Completed: " + str(record[5]) + 
                  " | Created At: " + record[6] + " | Updated At: " + record[7])
    else:
        print("No history available for this task.")
    
    conn.close()

# Main function to handle user inputs
def main():
    init_db()  # Initialize DB and ensure columns are added if needed

    while True:
        print("\nTask Management CLI")
        print("1. Add Task")
        print("2. List Tasks")
        print("3. Edit Task")
        print("4. Complete Task")
        print("5. View Task History")
        print("6. Exit")
        
        choice = int(input("Enter your choice (1-6): "))
        
        if choice == 1:
            name = input("Enter task name: ")
            column_name = input("Enter task column (optional): ")
            description = input("Enter task description: ")
            add_task(name, column_name, description)
        elif choice == 2:
            list_tasks()
        elif choice == 3:
            task_id = int(input("Enter task ID to edit: "))
            name = input("Enter new task name: ")
            column_name = input("Enter new task column (optional): ")
            description = input("Enter new task description: ")
            edit_task(task_id, name, column_name, description)
        elif choice == 4:
            task_id = int(input("Enter task ID to complete: "))
            complete_task(task_id)
        elif choice == 5:
            task_id = int(input("Enter task ID to view history: "))
            view_task_history(task_id)
        elif choice == 6:
            print("Exiting...")
            sys.exit(0)
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()
