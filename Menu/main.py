import sys
import os

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

from Main_System.main_system import execute_query,connect_db,close_connection
from Class.User import User
from Class.admin import Admin
from Class.Teacher import Teacher
from Class.Student import Student
from Class.Course import Course
from Class.Department import Department
from Class.Class_ import Class
import pwinput as pw

# ===================== LOGIN =====================
def login(conn):
    username = input("Username: ").strip()
    password = pw.pwinput("Password: ").strip()

    query = """
        SELECT userID, userName, password, role
        FROM User
        WHERE userName = %s AND password = %s
    """

    rows = execute_query(conn, query, (username, password))

    if not rows:
        raise ValueError("Sai tài khoản hoặc mật khẩu")

    row = rows[0]

    base_user = User(
        row["userID"],
        row["userName"],
        row["password"],
        row["role"]
    )

    role = row["role"].upper()

    if role == "ADMIN":
        return Admin(base_user)
    elif role == "TEACHER":
        return Teacher(base_user)
    elif role == "STUDENT":
        return Student(base_user)
    else:
        return base_user


# ===================== ADMIN MENU =====================
def admin_menu(admin: Admin):
    while True:
        print("""
===== ADMIN MENU =====
1. Manage User
2. Manage Department
3. Manage Course
4. Manage Class
5. Generate Report
6. View Info
7. Change Password
0. Logout
""")
        c = input("Chọn: ").strip()

        if c == "1":
            manage_user(admin)
        elif c == "2":
            manage_department(admin)
        elif c == "3":
            manage_course(admin)
        elif c == "4":
            manage_class(admin)
        elif c == "5":
            admin.generateReport()
        elif c == "6":
            admin.view_info()
        elif c == "7":
            change_password(admin)
        elif c == "0":
            break
        else:
            print("Lựa chọn không hợp lệ")


def manage_user(admin: Admin):
    print("""
--- MANAGE USER ---
1. Add User
2. Update User
3. Delete User
0. Back
""")
    choice = input("Chọn: ").strip()
    # TODO: Implement user management


def manage_department(admin: Admin):
    print("""
--- MANAGE DEPARTMENT ---
1. Add Department
2. Update Department
3. Delete Department
0. Back
""")
    choice = input("Chọn: ").strip()
    # TODO: Implement department management


def manage_course(admin: Admin):
    print("""
--- MANAGE COURSE ---
1. Add Course
2. Update Course
3. Delete Course
0. Back
""")
    choice = input("Chọn: ").strip()
    # TODO: Implement course management


def manage_class(admin: Admin):
    print("""
--- MANAGE CLASS ---
1. Add Class
2. Update Class
3. Delete Class
0. Back
""")
    choice = input("Chọn: ").strip()
    # TODO: Implement class management


def change_password(user: User):
    """
    Hàm đổi mật khẩu cho Admin, Teacher hoặc Student
    """
    try:
        username = input("Nhập username: ").strip()
        old_password = input("Nhập mật khẩu cũ: ").strip()
        new_password = input("Nhập mật khẩu mới: ").strip()
        confirm_password = input("Xác nhận mật khẩu mới: ").strip()
        
        if new_password != confirm_password:
            print("Mật khẩu xác nhận không trùng khớp")
            return
        
        if user.change_passWord(username, old_password, new_password):
            print("Đổi mật khẩu thành công")
        else:
            print("Đổi mật khẩu thất bại - Username hoặc mật khẩu cũ không đúng")
    except Exception as e:
        print(f"Lỗi: {e}")


# ===================== TEACHER MENU =====================
def teacher_menu(teacher: Teacher):
    while True:
        print("""
===== TEACHER MENU =====
1. View My Classes
2. Enter Score
3. Update Score
4. View Info
5. Change Password
0. Logout
""")
        c = input("Chọn: ").strip()

        if c == "1":
            teacher.viewClasses()
        elif c == "2":
            pass  # TODO: Implement enter score
        elif c == "3":
            pass  # TODO: Implement update score
        elif c == "4":
            teacher.view_info()
        elif c == "5":
            change_password(teacher)
        elif c == "0":
            break
        else:
            print("Lựa chọn không hợp lệ")


# ===================== STUDENT MENU =====================
def student_menu(student: Student):
    while True:
        print("""
===== STUDENT MENU =====
1. View Info
2. Join Course
3. View Grades
4. Calculate GPA
0. Logout
""")
        c = input("Chọn: ").strip()

        if c == "1":
            student.view_info()
        elif c == "2":
            pass  # TODO: Implement join course
        elif c == "3":
            student.ViewGrades()
        elif c == "4":
            student.calculateGPA()
        elif c == "0":
            break
        else:
            print("Lựa chọn không hợp lệ")


# ===================== MAIN =====================
def main():
    conn = connect_db()
    if conn is None:
        print("Không kết nối được CSDL")
        return

    try:
        user = login(conn)
        role = user.getRole().upper()

        if role == "ADMIN":
            admin_menu(user)  # type: ignore
        elif role == "TEACHER":
            teacher_menu(user)  # type: ignore
        elif role == "STUDENT":
            student_menu(user)  # type: ignore
        else:
            print("Role không hợp lệ")

    except Exception as e:
        print("Lỗi:", e)

    finally:
        close_connection(conn)


if __name__ == "__main__":
    main()
