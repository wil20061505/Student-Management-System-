from Class.User import User
from Class.Student import Student
from Class.Department import Department
from Class.Class_ import Class
from Class.Course import Course

from Main_System import main_system
conn = main_system.connect_db()
class Admin(User):
    def __init__(self,user : User):
        super().__init__(
            user.getUserId(),
            user.getUsername(),
            user.getPassword(),
            user.getRole()
        )

        query = """
            SELECT
                adminID
            FROM Admin
            WHERE userID = %s
        """

        rows = main_system.execute_query(
            conn,
            query,
            (user.getUserId(),)
        )

        if not rows:
            raise ValueError("Không tìm thấy Admin")

        row = rows[0]  # row là dict

        self.__StudentID = row["adminID"]

    def addStudent(self, student: Student):
        query = """
            INSERT INTO Student (
                studentID,
                fullName,
                email,
                phone,
                address,
                idNumber,
                status,
                userName
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        params = (
            student.getStudentID(),
            student.getFullname(),
            student.getEmail(),
            student.getPhone(),
            student.getAddress(),
            student.getIdnumber(),
            student.getStatus(),
            student.getUsername()
        )

        try:
            main_system.execute_update(conn,query, params)
            print("Thêm sinh viên thành công")
            return True
        except Exception as e:
            print(f"Lỗi thêm sinh viên: {e}")
            return False
    
    def deleteStudent(self,student:Student):
        conn = main_system.connect_db()
        if conn is None:
            return False

        student_id = student.getStudentID()

        # 1. Xóa bảng điểm
        if not main_system.execute_update(
            conn,
            "DELETE FROM AcademicResult WHERE studentID = %s",
            (student_id,)
        ):
            main_system.close_connection(conn)
            return False

        # 2. Xóa đăng ký học
        if not main_system.execute_update(
            conn,
            "DELETE FROM Enrollment WHERE studentID = %s",
            (student_id,)
        ):
            main_system.close_connection(conn)
            return False

        # 3. Xóa sinh viên
        if not main_system.execute_update(
            conn,
            "DELETE FROM Student WHERE studentID = %s",
            (student_id,)
        ):
            main_system.close_connection(conn)
            return False

        main_system.close_connection(conn)
        print("Xóa sinh viên thành công")
        return True

    def updateStudent(self,student: Student):
        
        print("=== CHỌN THÔNG TIN CẦN CHỈNH SỬA ===")
        print("1. Student ID")
        print("2. Full name")
        print("3. Email")
        print("4. Phone")
        print("5. Address")
        print("6. ID number")
        print("7. Status")

        choice = input("Chọn (1-7): ").strip()

        if choice == "1":
            new_value = input("Nhập Student ID mới: ").strip()
            student.edit_StudentID(new_value)
        elif choice == "2":
            new_value = input("Nhập Full name mới: ").strip()
            student.edit_Fullname(new_value)
        elif choice == "3":
            new_value = input("Nhập Email mới: ").strip()
            student.edit_Email(new_value)
        elif choice == "4":
            new_value = input("Nhập Phone mới: ").strip()
            student.edit_Phone(new_value)

        elif choice == "5":
            new_value = input("Nhập Address mới: ").strip()
            student.edit_Address(new_value)

        elif choice == "6":
            new_value = input("Nhập ID number mới: ").strip()
            student.edit_Idnumber(new_value)

        elif choice == "7":
            new_value = input("Nhập Status mới: ").strip()
            student.edit_Status(new_value)

        else:
            print("Lựa chọn không hợp lệ")
            return
        print("Cập nhật thông tin thành công")

    def manageStatus(self,student: Student,status):
        query = """
    UPDATE Student
    SET status = %s 
    WHERE studentID = %s;
"""
        params = (
            status,
            student.getStudentID()
        ) 
        try:
            main_system.execute_update(conn,query, params)
            print("Thêm sinh viên thái thành công")
            return True
        except Exception as e:
            print(f"Lỗi thêm thêm trạng thái: {e}")
            return False
        
    def addUser(self, user: User):
        query = """
            INSERT INTO User (userID, userName, password, role)
            VALUES (%s, %s, %s, %s)
        """
        return main_system.execute_update(
            conn, query,
            (user.getUserId(), user.getUsername(), user.getPassword(), user.getRole())
        )

    def updateUser(self, user: User):
        query = """
            UPDATE User
            SET userName = %s,
                password = %s,
                role = %s
            WHERE userID = %s
        """
        return main_system.execute_update(
            conn, query,
            (user.getUsername(), user.getPassword(), user.getRole(), user.getUserId())
        )

    def deleteUser(self, user: User):
        query = "DELETE FROM User WHERE userID = %s"
        return main_system.execute_update(conn, query, (user.getUserId(),))


    # ================= DEPARTMENT =================
    def addDepartment(self, department: Department):
        query = """
            INSERT INTO Department (departmentID, departmentName)
            VALUES (%s, %s)
        """
        return main_system.execute_update(
            conn, query,
            (department.getDepartmentID(), department.getDepartmentName())
        )

    def updateDepartment(self, department: Department):
        query = """
            UPDATE Department
            SET departmentName = %s
            WHERE departmentID = %s
        """
        return main_system.execute_update(
            conn, query,
            (department.getDepartmentName(), department.getDepartmentID())
        )

    def deleteDepartment(self, department: Department):
        query = "DELETE FROM Department WHERE departmentID = %s"
        return main_system.execute_update(conn, query, (department.getDepartmentID(),))


    # ================= COURSE =================
    def addCourse(self, course: Course):
        query = """
            INSERT INTO Course (courseID, courseCode, courseName, credit, departmentID)
            VALUES (%s, %s, %s, %s, %s)
        """
        return main_system.execute_update(
            conn, query,
            (
                course.get_courseID(),
                course.get_courseCode(),
                course.get_courseName(),
                course.get_credit(),
                course.get_departmentID()
            )
        )

    def updateCourse(self, course: Course):
        query = """
            UPDATE Course
            SET courseCode = %s,
                courseName = %s,
                credit = %s,
                departmentID = %s
            WHERE courseID = %s
        """
        return main_system.execute_update(
            conn, query,
            (
                course.get_courseID(),
                course.get_courseCode(),
                course.get_courseName(),
                course.get_credit(),
                course.get_departmentID()
            )
        )

    def deleteCourse(self, course: Course):
        query = "DELETE FROM Course WHERE courseID = %s"
        return main_system.execute_update(conn, query, (course.get_courseID(),))


    # ================= CLASS =================
    def addClass(self, cls: Class):
        query = """
            INSERT INTO Class (classID, schedule, maxStudent, courseID, instructorID, roomID)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        return main_system.execute_update(
            conn, query,
            (
                cls.getClassID(),
                cls.getSchedule(),
                cls.getMaxStudent(),
                cls.getCourseID(),
                cls.getInstructorID(),
                cls.getRoomID()
            )
        )

    def updateClass(self, cls: Class):
        query = """
            UPDATE Class
            SET schedule = %s,
                maxStudent = %s,
                courseID = %s,
                instructorID = %s,
                roomID = %s
            WHERE classID = %s
        """
        return main_system.execute_update(
            conn, query,
            (
                cls.getSchedule(),
                cls.getMaxStudent(),
                cls.getCourseID(),
                cls.getInstructorID(),
                cls.getRoomID(),
                cls.getClassID()
            )
        )

    def deleteClass(self, cls: Class):
        query = "DELETE FROM Class WHERE classID = %s"
        return main_system.execute_update(conn, query, (cls.getClassID(),))


    # ================= REPORT =================
    def generateReport(self):
        query = """
            SELECT
                d.departmentName,
                COUNT(DISTINCT c.courseID) AS totalCourses,
                COUNT(DISTINCT cl.classID) AS totalClasses,
                COUNT(DISTINCT e.studentID) AS totalStudents
            FROM Department d
            LEFT JOIN Course c ON d.departmentID = c.departmentID
            LEFT JOIN Class cl ON c.courseID = cl.courseID
            LEFT JOIN Enrollment e ON cl.classID = e.classID
            GROUP BY d.departmentID
        """
        return main_system.execute_query(conn, query)