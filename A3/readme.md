# Task Management CLI Tool

## Overview
The Task Management CLI Tool is a command-line application that allows users to efficiently manage their tasks. Users can add, edit, and complete tasks while also benefiting from version control to track changes and maintain a task history.

## Features
- **Add Tasks**: Users can add new tasks with descriptions and due dates.
- **Edit Tasks**: Modify existing tasks to update details.
- **Complete Tasks**: Mark tasks as completed.
- **Task History**: View a history of changes made to tasks.
- **Version Control**: Keep track of task modifications and maintain a record of updates.

## Installation
### Prerequisites
Ensure you have the following installed on your system:
- Python (3.x recommended)
- Git (for version control functionality)

### Steps
1. Clone the repository:
   ```sh
   git clone https://github.com/RishikaSur/SE_Lab_2025_A1_03_Repo.git
   cd task-management-cli
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Run the tool:
   ```sh
   python task_manager.py
   ```

## Usage
### Adding a Task
```sh
python task_manager.py add "Complete project report" --due 2025-04-10
```

### Editing a Task
```sh
python task_manager.py edit 1 --description "Update project report draft"
```

### Completing a Task
```sh
python task_manager.py complete 1
```

### Viewing Task History
```sh
python task_manager.py history
```

## File Structure
📂 task-management-cli
│── task_manager.py    # Main script with task management functionality
│── tasks.db           # SQLite database (auto-generated)
│── readme.md          # Project documentation
│── .gitignore         # Git ignore file
│── requirements.txt   # Dependencies file

## Contributing
1. Fork the repository.
2. Create a new branch: `git checkout -b feature-branch`
3. Commit your changes: `git commit -m "Add new feature"`
4. Push to the branch: `git push origin feature-branch`
5. Create a Pull Request.

## License
This project is licensed under the MIT License. See `LICENSE` for details.

## Contact
For any inquiries, please reach out to mayankrathi3009@gmail.com.

