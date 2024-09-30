# attendance.py

import pymysql
from datetime import datetime

def connect_db():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='root',
        database='student_marks_management'
    )

def create_tables():
    mydb = connect_db()
    my_cursor = mydb.cursor()

    my_cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INT PRIMARY KEY,
        name VARCHAR(100),
        math_marks INT,
        science_marks INT,
        english_marks INT
    );
    """)

    my_cursor.execute("""
    CREATE TABLE IF NOT EXISTS attendance (
        id INT,
        date DATE,
        status ENUM('Present', 'Absent'),
        PRIMARY KEY (id, date),
        FOREIGN KEY (id) REFERENCES students(id) ON DELETE CASCADE
    );
    """)

    mydb.commit()
    my_cursor.close()
    mydb.close()

def add_or_update_student():
    mydb = connect_db()
    my_cursor = mydb.cursor()

    id = int(input("Enter student ID: "))
    name = input("Enter name of the student: ")

    my_cursor.execute("SELECT * FROM students WHERE id = %s", (id,))
    result = my_cursor.fetchone()

    if result:
        print("Student found. Updating grades.")
        math_marks = int(input("Enter math marks: "))
        science_marks = int(input("Enter science marks: "))
        english_marks = int(input("Enter English marks: "))

        sql_update = """
        UPDATE students
        SET name = %s, math_marks = %s, science_marks = %s, english_marks = %s
        WHERE id = %s
        """
        my_cursor.execute(sql_update, (name, math_marks, science_marks, english_marks, id))
    else:
        print("Adding new student.")
        math_marks = int(input("Enter math marks: "))
        science_marks = int(input("Enter science marks: "))
        english_marks = int(input("Enter English marks: "))

        sql_insert = """
        INSERT INTO students (id, name, math_marks, science_marks, english_marks)
        VALUES (%s, %s, %s, %s, %s)
        """
        my_cursor.execute(sql_insert, (id, name, math_marks, science_marks, english_marks))

    mydb.commit()
    print("Record added/updated successfully.")

    my_cursor.close()
    mydb.close()

def record_attendance():
    mydb = connect_db()
    my_cursor = mydb.cursor()

    id = int(input("Enter student ID for attendance: "))
    date = datetime.now().date()
    status = input("Enter attendance status (Present/Absent): ")

    sql_insert = """
    INSERT INTO attendance (id, date, status)
    VALUES (%s, %s, %s)
    ON DUPLICATE KEY UPDATE status = %s;
    """
    my_cursor.execute(sql_insert, (id, date, status, status))

    mydb.commit()
    print("Attendance recorded successfully.")

    my_cursor.close()
    mydb.close()

def display_records():
    mydb = connect_db()
    my_cursor = mydb.cursor()
    my_cursor.execute("SELECT * FROM students")
    records = my_cursor.fetchall()
    print("Current records in the database:")
    for record in records:
        print(f"ID: {record[0]}, Name: {record[1]}, Math: {record[2]}, Science: {record[3]}, English: {record[4]}")
    my_cursor.close()
    mydb.close()

def display_attendance():
    mydb = connect_db()
    my_cursor = mydb.cursor()
    my_cursor.execute("SELECT * FROM attendance")
    records = my_cursor.fetchall()
    print("Attendance Records:")
    for record in records:
        print(f"ID: {record[0]}, Date: {record[1]}, Status: {record[2]}")
    my_cursor.close()
    mydb.close()

# attendance.py (Add this function to the existing code)

def generate_class_record():
    mydb = connect_db()
    my_cursor = mydb.cursor()

    sql = """
    SELECT s.id, s.name, s.math_marks, s.science_marks, s.english_marks, 
           a.date, a.status 
    FROM students s
    LEFT JOIN attendance a ON s.id = a.id
    ORDER BY s.id, a.date;
    """
    
    my_cursor.execute(sql)
    records = my_cursor.fetchall()

    print("\nClass Record:")
    print("ID\tName\tMath\tScience\tEnglish\tDate\t\tStatus")
    print("=" * 70)
    
    current_id = None
    for record in records:
        if current_id != record[0]:
            print(f"{record[0]}\t{record[1]}\t{record[2]}\t{record[3]}\t{record[4]}\t", end="")
            current_id = record[0]
        else:
            print("\t\t\t\t\t", end="")  # Keep spacing for grades
        
        if record[5]:
            print(f"{record[5]}\t{record[6]}")
        else:
            print("\t\t")

    my_cursor.close()
    mydb.close()

# attendance.py (Add this function to the existing code)

def view_grades():
    mydb = connect_db()
    my_cursor = mydb.cursor()

    id = int(input("Enter student ID to access grades: "))

    my_cursor.execute("SELECT name, math_marks, science_marks, english_marks FROM students WHERE id = %s", (id,))
    student = my_cursor.fetchone()

    if student:
        print(f"\nGrades for {student[0]} (ID: {id}):")
        print(f"Math: {student[1]}")
        print(f"Science: {student[2]}")
        print(f"English: {student[3]}")
    else:
        print("Student ID not found.")

    my_cursor.close()
    mydb.close()

