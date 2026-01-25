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

    def view_info(self):
        """
        Hiển thị thông tin của Admin
        """
        print("=== THÔNG TIN ADMIN ===")
        print(f"User ID: {self.getUserId()}")
        print(f"Username: {self.getUsername()}")
        print(f"Admin ID: {self.__StudentID}")
        print(f"Role: {self.getRole()}")
        print("=" * 30)

    def addStudent(self,studentID,
                fullName,
                email,
                phone,
                address,
                idNumber,
                status,
                userName):
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
            studentID,
                fullName,
                email,
                phone,
                address,
                idNumber,
                status,
                userName )

        try:
            main_system.execute_update(conn,query, params)
            print("Thêm sinh viên thành công")
            return True
        except Exception as e:
            print(f"Lỗi thêm sinh viên: {e}")
            return False
    
    def deleteStudent(self,student_id ):
        conn = main_system.connect_db()
        if conn is None:
            return False

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

    def updateStudent(self, studentId, fullName, email, phone, address, idNumber, status, userName):
        query = """
            UPDATE Student
            SET fullName = %s,
                email = %s,
                phone = %s,
                address = %s,
                idNumber = %s,
                status = %s,
                userName = %s
            WHERE studentID = %s
        """
        params = (fullName, email, phone, address, idNumber, status, userName, studentId)
        
        try:
            main_system.execute_update(conn, query, params)
            print("Cập nhật sinh viên thành công")
            return True
        except Exception as e:
            print(f"Lỗi cập nhật sinh viên: {e}")
            return False

    def manageStatus(self,studentId,status):
        query = """
    UPDATE Student
    SET status = %s 
    WHERE studentID = %s;
"""
        params = (
            status,
            studentId
        ) 
        try:
            main_system.execute_update(conn,query, params)
            print("Thêm sinh viên thái thành công")
            return True
        except Exception as e:
            print(f"Lỗi thêm thêm trạng thái: {e}")
            return False
        
    def addUser(self, userID, userName, password, role):
        query = """
            INSERT INTO User (userID, userName, password, role)
            VALUES (%s, %s, %s, %s)
        """
        return main_system.execute_update(
            conn, query,
            (userID, userName, password, role)
        )

    def updateUser(self, userName,
                password,
                role,
        userID):
        query = """
            UPDATE User
            SET userName = %s,
                password = %s,
                role = %s
            WHERE userID = %s
        """
        return main_system.execute_update(
            conn, query,
            (userName,
                password,
                role,
        userID)
        )

    def deleteUser(self, userId):
        query = "DELETE FROM User WHERE userID = %s"
        return main_system.execute_update(conn, query, (userId,))


    # ================= DEPARTMENT =================
    def addDepartment(self ,departmentid,DepartmentName ):
        query = """
            INSERT INTO Department (departmentID, departmentName)
            VALUES (%s, %s)
        """
        return main_system.execute_update(
            conn, query,
            (departmentid,DepartmentName)
        )

    def updateDepartment(self,DepartmentName, departmentid):
        query = """
            UPDATE Department
            SET departmentName = %s
            WHERE departmentID = %s
        """
        return main_system.execute_update(
            conn, query,
            (DepartmentName, departmentid)
        )

    def deleteDepartment(self, DepartmentID):
        query = "DELETE FROM Department WHERE departmentID = %s"
        return main_system.execute_update(conn, query, (DepartmentID,))


    # ================= COURSE =================
    def addCourse(
            self,
              courseID,
                courseCode,
                courseName,
                credit,
                departmentID):
        query = """
            INSERT INTO Course (courseID, courseCode, courseName, credit, departmentID)
            VALUES (%s, %s, %s, %s, %s)
        """
        return main_system.execute_update(
            conn, query,
            (
                courseID,
                courseCode,
                courseName,
                credit,
                departmentID
            )
        )

    def updateCourse(self,
              courseID,
                courseCode,
                courseName,
                credit,
                departmentID):
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
             courseCode ,
                courseName,
                credit,
                departmentID ,
            courseID
            )
        )

    def deleteCourse(self, courseID):
        query = "DELETE FROM Course WHERE courseID = %s"
        return main_system.execute_update(conn, query, (courseID,))


    # ================= CLASS =================
    def addClass(self,
                ClassID,
                Schedule,
                MaxStudent,
                CourseID,
                InstructorID,
                RoomID
            ):
        query = """
            INSERT INTO Class (classID, schedule, maxStudent, courseID, instructorID, roomID)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        return main_system.execute_update(
            conn, query,
            (
                ClassID,
                Schedule,
                MaxStudent,
                CourseID,
                InstructorID,
                RoomID
            )
        )

    def updateClass(self, schedule, maxStudent,courseID,instructorID ,roomID ,classID ):
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
                schedule,
                maxStudent,
                courseID,
                instructorID ,
                roomID ,
            classID 
            )
        )

    def deleteClass(self, ClassID):
        query = "DELETE FROM Class WHERE classID = %s"
        return main_system.execute_update(conn, query, (ClassID,))


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
        rows = main_system.execute_query(conn, query)
        if not rows:
            raise ValueError("Không tìm thấy Admin")

        row = rows[0]  # row là dict
        print(f"departmentName: {row["departmentName"]}")
        print(f"totalCourses: {row["totalCourses"]}")
        print(f"totalClasses: {row["totalClasses"]}")
        print(f"totalStudents: {row["totalStudents"]}")