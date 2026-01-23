from User import User
from Student import Student
from Main_System import main
conn = main.connect_db()
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
                adminID,
            FROM Admin
            WHERE userID = %s
        """

        rows = main.execute_query(
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
            main.execute_update(conn,query, params)
            print("Thêm sinh viên thành công")
            return True
        except Exception as e:
            print(f"Lỗi thêm sinh viên: {e}")
            return False
    
    def deleteStudent(self,student:Student):
        conn = main.connect_db()
        if conn is None:
            return False

        student_id = student.getStudentID()

        # 1. Xóa bảng điểm
        if not main.execute_update(
            conn,
            "DELETE FROM AcademicResult WHERE studentID = %s",
            (student_id,)
        ):
            main.close_connection(conn)
            return False

        # 2. Xóa đăng ký học
        if not main.execute_update(
            conn,
            "DELETE FROM Enrollment WHERE studentID = %s",
            (student_id,)
        ):
            main.close_connection(conn)
            return False

        # 3. Xóa sinh viên
        if not main.execute_update(
            conn,
            "DELETE FROM Student WHERE studentID = %s",
            (student_id,)
        ):
            main.close_connection(conn)
            return False

        main.close_connection(conn)
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
