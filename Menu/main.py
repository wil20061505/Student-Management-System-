import sys
import os
import pwinput as pw

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

from Main_System.main_system import execute_query, connect_db, close_connection
from Class.User import User
from Class.admin import Admin
from Class.Teacher import Teacher
from Class.Student import Student

# ===================== LOGIN =====================
def login(conn):
    print("===== LOGIN =====")
    username = input("Username: ").strip()
    password = pw.pwinput("Password: ").strip()

    query = """
        SELECT userID, userName, password, role
        FROM User
        WHERE userName = %s AND password = %s
    """
    rows = execute_query(conn, query, (username, password))

    if not rows:
        raise ValueError("Invalid username or password")

    row = rows[0]
    base_user = User(row["userID"], row["userName"], row["password"], row["role"])
    role = row["role"].upper()

    if role == "ADMIN":
        return Admin(base_user)
    elif role == "TEACHER":
        return Teacher(base_user)
    elif role == "STUDENT":
        return Student(base_user)
    return base_user


# ===================== ADMIN MENU =====================
def admin_menu(admin: Admin):
    while True:
        print("""
===== ADMIN MENU =====
1. Manage Users
2. Manage Departments
3. Manage Courses
4. Manage Classes
5. Generate Report
6. View Info
7. Change Password
8. Logout
9. Backup Database
10. Restore Database
0. Exit
""")
        choice = input("Select: ").strip()

        if choice == "1":
            manage_user(admin)
        elif choice == "2":
            manage_department(admin)
        elif choice == "3":
            manage_course(admin)
        elif choice == "4":
            manage_class(admin)
        elif choice == "5":
            admin.generateReport()
        elif choice == "6":
            admin.view_info()
        elif choice == "7":
            change_password(admin)
        elif choice == "8":
            return "LOGOUT"

        elif choice == "9":
            admin.backupDatabase()
        elif choice == "10":
            admin.restoreDatabase()
        elif choice == "0":
            sys.exit(0)
        else:
            print("Invalid choice")


def manage_user(admin: Admin):
    print("""
--- USER MANAGEMENT ---
1. Add User
2. Update User
3. Delete User
0. Back
""")
    choice = input("Select: ").strip()

    if choice == "1":
        userID = input("User ID: ").strip()
        userName = input("Username: ").strip()
        password = input("Password: ").strip()
        role = input("Role (ADMIN/TEACHER/STUDENT): ").strip().upper()
        admin.addUser(userID, userName, password, role)

    elif choice == "2":
        userID = input("User ID: ").strip()
        userName = input("New Username: ").strip()
        password = input("New Password: ").strip()
        role = input("New Role: ").strip().upper()
        admin.updateUser(userName, password, role, userID)

    elif choice == "3":
        userID = input("User ID: ").strip()
        admin.deleteUser(userID)


def manage_department(admin: Admin):
    print("""
--- DEPARTMENT MANAGEMENT ---
1. Add Department
2. Update Department
3. Delete Department
0. Back
""")
    choice = input("Select: ").strip()

    if choice == "1":
        dept_id = input("Department ID: ").strip()
        dept_name = input("Department Name: ").strip()
        admin.addDepartment(dept_id, dept_name)

    elif choice == "2":
        dept_id = input("Department ID: ").strip()
        dept_name = input("New Department Name: ").strip()
        admin.updateDepartment(dept_id, dept_name)

    elif choice == "3":
        dept_id = input("Department ID: ").strip()
        admin.deleteDepartment(dept_id)


def manage_course(admin: Admin):
    print("""
--- COURSE MANAGEMENT ---
1. Add Course
2. Update Course
3. Delete Course
0. Back
""")
    choice = input("Select: ").strip()

    if choice == "1":
        admin.addCourse(
            input("Course ID: ").strip(),
            input("Course Code: ").strip(),
            input("Course Name: ").strip(),
            int(input("Credit: ").strip()),
            input("Department ID: ").strip()
        )

    elif choice == "2":
        admin.updateCourse(
            input("Course ID: ").strip(),
            input("Course Code: ").strip(),
            input("New Course Name: ").strip(),
            int(input("Credit: ").strip()),
            input("Department ID: ").strip()
        )

    elif choice == "3":
        admin.deleteCourse(input("Course ID: ").strip())


def manage_class(admin: Admin):
    print("""
--- CLASS MANAGEMENT ---
1. Add Class
2. Update Class
3. Delete Class
0. Back
""")
    choice = input("Select: ").strip()

    if choice == "1":
        admin.addClass(
            input("Class ID: ").strip(),
            input("Schedule: ").strip(),
            int(input("Max Students: ").strip()),
            input("Course ID: ").strip(),
            input("Instructor ID: ").strip(),
            input("Room ID: ").strip()
        )

    elif choice == "2":
        admin.updateClass(
            input("Schedule: ").strip(),
            int(input("Max Students: ").strip()),
            input("Course ID: ").strip(),
            input("Instructor ID: ").strip(),
            input("Room ID: ").strip(),
            input("Class ID: ").strip()
        )

    elif choice == "3":
        admin.deleteClass(input("Class ID: ").strip())


# ===================== PASSWORD =====================
def change_password(user: User):
    old_pass = pw.pwinput("Old password: ").strip()
    new_pass = pw.pwinput("New password: ").strip()
    confirm = pw.pwinput("Confirm new password: ").strip()

    if new_pass != confirm:
        print("Password confirmation does not match")
        return

    if user.change_passWord(user.getUsername(), old_pass, new_pass):
        print("Password changed successfully")
    else:
        print("Failed to change password")

# ===================== TEACHER MENU =====================
def teacher_menu(teacher: Teacher):
    while True:
        print("""
===== TEACHER MENU =====
1. View My Classes
2. Enter Student Score
3. Update Student Score
4. View Personal Info
5. Change Password
8. Logout
0. Exit
""")
        choice = input("Select: ").strip()

        if choice == "1":
            teacher.viewClasses()

        elif choice == "2":
            studentID = input("Student ID: ").strip()
            courseID = input("Course ID: ").strip()
            score = input("Score: ").strip()
            teacher.enterScore(studentID, courseID, score)

        elif choice == "3":
            studentID = input("Student ID: ").strip()
            courseID = input("Course ID: ").strip()
            teacher.updateScore(studentID, courseID)

        elif choice == "4":
            teacher.view_info()

        elif choice == "5":
            change_password(teacher)

        elif choice == "8":
            return "LOGOUT"

        elif choice == "0":
            sys.exit(0)

        else:
            print("Invalid choice")
# ===================== STUDENT MENU =====================
def student_menu(student: Student):
    while True:
        print("""
===== STUDENT MENU =====
1. View Personal Info
2. Join Course
3. View Grades
4. Calculate GPA
5. Edit Profile
6. Change Password
8. Logout
0. Exit
""")
        choice = input("Select: ").strip()

        if choice == "1":
            student.view_info()

        elif choice == "2":
            courseID = input("Course ID: ").strip()
            student.joinCourse(courseID)

        elif choice == "3":
            student.ViewGrades()

        elif choice == "4":
            student.calculateGPA()

        elif choice == "5":
            Username = input("Confirm password:").strip()
            password = pw.pwinput("Confirm password: ").strip()
            student.edit_info(Username, password)

        elif choice == "6":
            change_password(student)

        elif choice == "8":
            return "LOGOUT"

        elif choice == "0":
            sys.exit(0)

        else:
            print("Invalid choice")

# ===================== MAIN =====================
def main():
    conn = connect_db()
    if not conn:
        print("Database connection failed")
        return

    try:
        while True:
            try:
                user = login(conn)
            except ValueError as e:
                print(e)
                continue

            role = user.getRole().upper()
            if role == "ADMIN":
                result = admin_menu(user) # type: ignore
            elif role == "TEACHER":
                result = teacher_menu(user) # type: ignore
            elif role == "STUDENT":
                result = student_menu(user) # type: ignore

            if result != "LOGOUT":
                break
    finally:
        close_connection(conn)


if __name__ == "__main__":
    main()
