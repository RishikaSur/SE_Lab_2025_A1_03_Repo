# Marks Management System with Git

This repository contains the solution for Assignment 2 of the Software Engineering Lab 2025 course. The project implements a command-line marks management system with Git-like version control using Python and SQLite3.

## Files

- `marks_management.py`: Main Python script with CLI interface
- `marks.db`: SQLite3 database (automatically created on first run)

## Key Features

- Add new Student details with their Roll Number and Name.
- Subject teachers can update marks as needed before the final submission.
- Teachers can view all student details but only edit the marks for their subject by using their own Teacher Id.
- The database is sorted by total marks of the students.

## Installation

1. Clone the repository:
```bash
git clone https://github.com/itsjustasemicolon/SE_Lab_2025_A1_04.git
```

2. Navigate to project directory:
```bash
 cd .\SE_Lab_2025_A1_04\A2
```

3. Run the application:
```bash
python3 marks_management.py    # Linux/MacOS
py marks_management.py         # Windows
```

## Usage

Once the script is running, follow the on-screen prompts to perform various operations such as adding, updating, or viewing details.

## Database Design

### Core Tables
```sql
marks (
  roll_number INTEGER PRIMARY KEY,
  name TEXT,
  math_marks INTEGER DEFAULT 0,
  science_marks INTEGER DEFAULT 0,
  english_marks INTEGER DEFAULT 0,
  total_marks INTEGER DEFAULT 0
)
```

## License

This project is licensed under the MIT License - LICENSE
