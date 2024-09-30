# main.py (Update the existing code)

from attendance import create_tables, add_or_update_student, record_attendance, display_records, display_attendance, generate_class_record, view_grades

def main():
    create_tables()
    while True:
        print("\nMenu:")
        print("1. Add/Update Student Grades")
        print("2. Record Attendance")
        print("3. Display All Student Records")
        print("4. Display Attendance Records")
        print("5. Generate Class Record")
        print("6. View Student Grades")
        print("7. Exit")

        choice = input("Select an option (1-7): ")

        if choice == '1':
            add_or_update_student()
        elif choice == '2':
            record_attendance()
        elif choice == '3':
            display_records()
        elif choice == '4':
            display_attendance()
        elif choice == '5':
            generate_class_record()
        elif choice == '6':
            view_grades()
        elif choice == '7':
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
