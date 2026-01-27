from Class.User import User
from Class.Student import Student
from Class.Department import Department
from Class.Class_ import Class
from Class.Course import Course
import os
from datetime import datetime
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

        self.__adminID = row["adminID"]

    def view_info(self):
        """
        Hiển thị thông tin của Admin
        """
        print("=== THÔNG TIN ADMIN ===")
        print(f"User ID: {self.getUserId()}")
        print(f"Username: {self.getUsername()}")
        print(f"Admin ID: {self.__adminID}")
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
                COUNT(DISTINCT e.studentID) AS totalStudents,
                COUNT(DISTINCT cl.instructorID) AS totalTeachers
            FROM Department d
            LEFT JOIN Course c ON d.departmentID = c.departmentID
            LEFT JOIN Class cl ON c.courseID = cl.courseID
            LEFT JOIN Enrollment e ON cl.classID = e.classID
            GROUP BY d.departmentID, d.departmentName
            ORDER BY d.departmentName
        """

        rows = main_system.execute_query(conn, query)

        if not rows:
            print("Không có dữ liệu báo cáo")
            return

        print("\n===== SYSTEM REPORT BY DEPARTMENT =====")
        for row in rows:
            print(f"""
    Department       : {row['departmentName']}
    Total Courses    : {row['totalCourses']}
    Total Classes    : {row['totalClasses']}
    Total Students   : {row['totalStudents']}
    Total Teachers   : {row['totalTeachers']}
    ---------------------------------------
    """)
    def backupDatabase(self):
        """
        Backup toàn bộ database ra file .sql
        """
        try:
            # thông tin DB (đồng bộ với main_system)
            DB_NAME = "DB_Student_Management_System"
            DB_USER = "root"
            DB_PASSWORD = "dat0377324546"
            DB_HOST = "host.docker.internal"

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_dir = "backup"
            os.makedirs(backup_dir, exist_ok=True)

            backup_file = f"{backup_dir}/backup_{timestamp}.sql"

            command = (
                f"mysqldump -h {DB_HOST} -u {DB_USER} "
                f"-p{DB_PASSWORD} {DB_NAME} > {backup_file}"
            )

            os.system(command)

            print(f"Backup thành công: {backup_file}")
            return True

        except Exception as e:
            print(f"Lỗi backup: {e}")
            return False
    def restoreDatabase(self):
        """
        Restore database từ file backup mới nhất
        """
        try:
            DB_NAME = "DB_Student_Management_System"
            DB_USER = "root"
            DB_PASSWORD = "dat0377324546"
            DB_HOST = "host.docker.internal"

            backup_dir = "backup"
            files = sorted(os.listdir(backup_dir), reverse=True)

            if not files:
                print("Không tìm thấy file backup")
                return False

            latest_backup = os.path.join(backup_dir, files[0])

            command = (
                f"mysql -h {DB_HOST} -u {DB_USER} "
                f"-p{DB_PASSWORD} {DB_NAME} < {latest_backup}"
            )

            os.system(command)

            print(f"Restore thành công từ: {latest_backup}")
            return True

        except Exception as e:
            print(f"Lỗi restore: {e}")
            return False
