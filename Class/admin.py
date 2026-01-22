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
