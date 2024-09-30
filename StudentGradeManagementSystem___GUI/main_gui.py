import tkinter as tk
from tkinter import messagebox, simpledialog
import pymysql

def connect_db():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='root',
        database='student_marks_management'
    )

def add_student():
    mydb = connect_db()
    my_cursor = mydb.cursor()

    try:
        id = int(simpledialog.askstring("Input", "Enter student ID:"))
        name = simpledialog.askstring("Input", "Enter student name:")
        math_marks = int(simpledialog.askstring("Input", "Enter math marks:"))
        science_marks = int(simpledialog.askstring("Input", "Enter science marks:"))
        english_marks = int(simpledialog.askstring("Input", "Enter English marks:"))

        sql = """
        INSERT INTO students (id, name, math_marks, science_marks, english_marks)
        VALUES (%s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE name=%s, math_marks=%s, science_marks=%s, english_marks=%s;
        """
        my_cursor.execute(sql, (id, name, math_marks, science_marks, english_marks, name, math_marks, science_marks, english_marks))
        mydb.commit()
        messagebox.showinfo("Success", "Student record added/updated successfully.")
    except Exception as e:
        messagebox.showerror("Error", str(e))
    finally:
        my_cursor.close()
        mydb.close()

def view_grades():
    mydb = connect_db()
    my_cursor = mydb.cursor()

    try:
        id = int(simpledialog.askstring("Input", "Enter student ID to view grades:"))
        my_cursor.execute("SELECT name, math_marks, science_marks, english_marks FROM students WHERE id = %s", (id,))
        student = my_cursor.fetchone()

        if student:
            messagebox.showinfo("Grades", f"Grades for {student[0]}:\nMath: {student[1]}\nScience: {student[2]}\nEnglish: {student[3]}")
        else:
            messagebox.showerror("Error", "Student ID not found.")
    except Exception as e:
        messagebox.showerror("Error", str(e))
    finally:
        my_cursor.close()
        mydb.close()

def record_attendance():
    mydb = connect_db()
    my_cursor = mydb.cursor()

    try:
        id = int(simpledialog.askstring("Input", "Enter student ID for attendance:"))
        status = simpledialog.askstring("Input", "Enter attendance status (Present/Absent):")

        sql = """
        INSERT INTO attendance (id, date, status)
        VALUES (%s, CURDATE(), %s)
        ON DUPLICATE KEY UPDATE status = %s;
        """
        my_cursor.execute(sql, (id, status, status))
        mydb.commit()
        messagebox.showinfo("Success", "Attendance recorded successfully.")
    except Exception as e:
        messagebox.showerror("Error", str(e))
    finally:
        my_cursor.close()
        mydb.close()
###############
def show_all_records():
    mydb = connect_db()
    if not mydb:
        return

    my_cursor = mydb.cursor()
    try:
        my_cursor.execute("SELECT id, name, math_marks, science_marks, english_marks FROM students")
        records = my_cursor.fetchall()

        if records:
            records_str = "\n".join([f"ID: {rec[0]}, Name: {rec[1]}, Math: {rec[2]}, Science: {rec[3]}, English: {rec[4]}" for rec in records])
            messagebox.showinfo("All Student Records", records_str)
        else:
            messagebox.showinfo("All Student Records", "No records found.")
    except Exception as e:
        messagebox.showerror("Error", str(e))
    finally:
        my_cursor.close()
        mydb.close()
##############
def create_app():
    root = tk.Tk()
    root.title("Student Grade Management System")

    tk.Label(root, text="Welcome to Student Grade Management System", font=("Helvetica", 16)).pack(pady=10)

    tk.Button(root, text="Add/Update Student", command=add_student, width=30).pack(pady=5)
    tk.Button(root, text="View Student Grades", command=view_grades, width=30).pack(pady=5)
    tk.Button(root, text="Record Attendance", command=record_attendance, width=30).pack(pady=5)
    tk.Button(root, text="Show All Records", command=show_all_records, width=30).pack(pady=5)  # New button for showing all records
    tk.Button(root, text="Exit", command=root.destroy, width=30).pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    create_app()
