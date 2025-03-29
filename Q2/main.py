import sqlite3

def initialize_database():
    conn = sqlite3.connect('marks.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS marks (
                    roll_number INTEGER PRIMARY KEY,
                    name TEXT,
                    math_marks INTEGER DEFAULT 0,
                    science_marks INTEGER DEFAULT 0,
                    english_marks INTEGER DEFAULT 0,
                    total_marks INTEGER DEFAULT 0
                )''')
    conn.commit()
    conn.close()

teachers={
    't1':'math',
    't2':'science',
    't3':'english'
}

def add_student(roll_number, name):
    conn = sqlite3.connect('marks.db')
    c = conn.cursor()
    c.execute("INSERT INTO marks (roll_number, name, math_marks, science_marks, english_marks, total_marks) VALUES (?, ?, 0, 0, 0, 0)",
              (roll_number, name))
    conn.commit()
    conn.close()

def update_marks(roll_number, subject, marks):
        valid_subjects = {"math", "science", "english"}
        if subject not in valid_subjects:
                print("Invalid subject! Choose from math, science, or english.")
                return

        column_name = subject + "_marks"

        conn = sqlite3.connect('marks.db')
        c = conn.cursor()
        query = "UPDATE marks SET " + column_name + " = ? WHERE roll_number = ?"
        c.execute(query, (marks, roll_number))
        c.execute("""
                UPDATE marks
                SET total_marks = COALESCE(math_marks, 0) + COALESCE(science_marks, 0) + COALESCE(english_marks, 0)
                WHERE roll_number = ?
                """, (roll_number,))
        conn.commit()
        conn.close()

def check_roll_number(roll_number):
        conn=sqlite3.connect('marks.db')
        c = conn.cursor()
        c.execute("Select * FROM marks WHERE roll_number=?",(roll_number,))
        result = c.fetchone()

        if not result:
                print("Roll number " + str(roll_number) + "does not exist in the database")
                return False
        else:
                return True
        conn.close()

def sort_database():
    conn = sqlite3.connect('marks.db')
    c = conn.cursor()
    c.execute("SELECT * FROM marks ORDER BY total_marks DESC")
    result = c.fetchall()
    conn.close()
    return result

def display_students(students):
    print("\n{:<12} {:<20} {:<12} {:<12} {:<12} {:<12}".format(
        "Roll Number", "Name", "Math Marks", "Science Marks", "English Marks", "Total Marks"))
    print("-" * 80)

    for student in students:
        print("{:<12} {:<20} {:<12} {:<12} {:<12} {:<12}".format(*student))
    print()

def display_menu():
    print("\nMenu:")
    print("1. Add Student")
    print("2. Update Marks")
    print("3. View Student Information")
    print("4. Exit")

def main():
        initialize_database()

        while True:
                display_menu()
                choice = input("Enter your choice: ")

                if choice == 1:
                        roll_number = int(input("Enter roll number: "))
                        name = input("Enter name: ")
                        add_student(roll_number, name)
                        print("Student added successfully.")

                elif choice == 2:
                        tid = input("Enter your teacher id : ").strip().lower()
                        if tid in teachers:
                                while True:
                                        roll_number = int(input("Enter roll number: "))
                                        res=check_roll_number(roll_number)
                                        if res==True:
                                                break
                                marks = int(input("Enter marks for " + teachers[tid] + ": "))
                                update_marks(roll_number, teachers[tid], marks)
                                print("Marks updated successfully.")
                        else:
                                print("Invalid Teacher ID entered. Access Denied")

                elif choice == 3:
                        students = sort_database()
                        display_students(students)

                elif choice == 4:
                        print("Exiting program.")
                        break

                else:
                        print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
