from Main_System import main_system
from Class.User import User
from Class.Student import Student
from  Class.Course import Course
conn = main_system.connect_db()
class Teacher(User):
    def __init__(self,user: User):
                # gọi constructor cha
        super().__init__(
            user.getUserId(),
            user.getUsername(),
            user.getPassword(),
            user.getRole()
        )

        query = """
            SELECT
        teacherID,
        fullName,
        email,
        userID,
        instructorID
            FROM Teacher
            WHERE userID = %s
        """

        rows = main_system.execute_query(
            conn,
            query,
            (user.getUserId(),)
            )
        
        if not rows:
            raise ValueError("Không tìm thấy Giảng viên")

        row = rows[0]  # row là dict

        self.__teacherID = row["teacherID"]
        self.__Fullname = row["fullName"]
        self.__Email = row["email"]
        self.__userID = row["userID"]
        self.__instructorID = row["instructorID"]

    # Getters
    def get_teacherID(self):
        return self.__teacherID
    
    def get_fullname(self):
        return self.__Fullname
    
    def get_email(self):
        return self.__Email
    
    def get_userID(self):
        return self.__userID
    
    def get_instructorID(self):
        return self.__instructorID
    
    # Setters
    def set_fullname(self, fullname):
        self.__Fullname = fullname
    
    def set_email(self, email):
        self.__Email = email
    
    def set_instructorID(self, instructorID):
        self.__instructorID = instructorID

    def view_info(self):
        """
        Hiển thị thông tin của Giáo viên
        """
        print("=== THÔNG TIN GIÁO VIÊN ===")
        print(f"User ID: {self.get_userID()}")
        print(f"Username: {self.getUsername()}")
        print(f"Teacher ID: {self.get_teacherID()}")
        print(f"Full Name: {self.get_fullname()}")
        print(f"Email: {self.get_email()}")
        print(f"Instructor ID: {self.get_instructorID()}")
        print(f"Role: {self.getRole()}")
        print("=" * 30)

# nhập điểm 
    def enterScore(self, student : Student , course : Course, score):
        if score >= 8.5:
            grade = "A"
        elif score >= 7.0:
            grade = "B"
        elif score >= 5.5:
            grade = "C"
        else:
            grade = "D"
        
        query = """
            INSERT INTO AcademicResult (studentID, courseID, score, grade)
            VALUES (%s, %s, %s, %s)
        """
        params = (
            student.getStudentID(),
            course.get_courseID(),
            score,
            grade
        )
        try:
            main_system.execute_update(conn, query, params)
            print("Nhập điểm thành công")
            return True
        except Exception as e:
            print(f"Nhập điểm không thành công: {e}")
            return False
        
    def updateScore(self, student: Student, course: Course):
        try:
            score = float(input("Nhập điểm mới: ").strip())
        except ValueError:
            print("Điểm không hợp lệ")
            return

        # Quy đổi điểm chữ
        if score >= 8.5:
            grade = "A"
        elif score >= 7.0:
            grade = "B"
        elif score >= 5.5:
            grade = "C"
        else:
            grade = "D"

        query = """
            UPDATE AcademicResult
            SET score = %s,
                grade = %s
            WHERE studentID = %s
            AND classID IN (
                SELECT classID
                FROM Class
                WHERE courseID = %s
            )
        """

        params =  (
                score,
                grade,
                student.getStudentID(),
                course.get_courseID()
            )
        success = main_system.execute_update(
            conn,
            query,
            params
        )

        if success:
            print("Cập nhật điểm thành công")
        else:
            print("Cập nhật điểm thất bại")

    def viewClasses(self):
        """
        Giáo viên xem các lớp mình phụ trách
        """

        query = """
            SELECT
                c.classID,
                c.schedule,
                c.maxStudent,
                co.courseCode,
                co.courseName,
                r.roomName
            FROM Class c
            JOIN Course co ON c.courseID = co.courseID
            JOIN ClassRoom r ON c.roomID = r.roomID
            WHERE c.instructorID = %s
        """

        rows = main_system.execute_query(
            conn,
            query,
            (self.get_instructorID(),)
        )

        if not rows:
            print("Giáo viên chưa phụ trách lớp nào")
            return

        print("=== DANH SÁCH LỚP PHỤ TRÁCH ===")
        for row in rows:
            print(
                f"Mã lớp: {row['classID']} | "
                f"Môn: {row['courseCode']} - {row['courseName']} | "
                f"Lịch: {row['schedule']} | "
                f"Phòng: {row['roomName']} | "
                f"Sĩ số tối đa: {row['maxStudent']}"
            )
