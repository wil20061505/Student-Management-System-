from Class.User import User
from Class.Course import Course
from Main_System import main_system
from datetime import date
conn = main_system.connect_db()
class Student(User):
    def __init__(self, user: User):
        # gọi constructor cha
        super().__init__(
            user.getUserId(),
            user.getUsername(),
            user.getPassword(),
            user.getRole()
        )

        query = """
            SELECT
                studentID,
                fullName,
                email,
                phone,
                address,
                idNumber,
                status
            FROM Student
            WHERE userID = %s
        """

        rows = main_system.execute_query(
            conn,
            query,
            (user.getUserId(),)
        )

        if not rows:
            raise ValueError("Không tìm thấy sinh viên")

        row = rows[0]  # dict

        self.__StudentID = row["studentID"]
        self.__Fullname = row["fullName"]
        self.__Email = row["email"]
        self.__phone = row["phone"]
        self.__address = row["address"]
        self.__Idnumber = row["idNumber"]
        self.__status = row["status"]

    # Getter và Setter cho StudentID
    def getStudentID(self):
        return self.__StudentID
    def setStudentID(self, StudentID):
        self.__StudentID = StudentID
    # Getter và Setter cho Fullname
    def getFullname(self):
        return self.__Fullname
    def setFullname(self, Fullname):
        self.__Fullname = Fullname
    # Getter và Setter cho Email
    def getEmail(self):
        return self.__Email
    def setEmail(self, Email):
        self.__Email = Email
    # Getter và Setter cho phone
    def getPhone(self):
        return self.__phone 
    def setPhone(self, Phone):
        self.__phone = Phone
    # Getter và Setter cho address
    def getAddress(self):
        return self.__address 
    def setAddress(self, address):
        self.__address = address
    # Getter và Setter cho Idnumber
    def getIdnumber(self):
        return self.__Idnumber  
    def setIdnumber(self, IDnumber):
        self.__Idnumber = IDnumber 
    # Getter và Setter cho status
    def getStatus(self):
        return self.__status
    def setStatus(self, status):
        self.__status = status
# xem thông tin sinh viên
    def view_info(self):
        print("=== THÔNG TIN SINH VIÊN ===")
        print(f"Student ID: {self.getStudentID()}")
        print(f"Full Name: {self.getFullname()}")
        print(f"Email: {self.getEmail()}")
        print(f"Phone: {self.getPhone()}")
        print(f"Address: {self.getAddress()}")
        print(f"ID Number: {self.getIdnumber()}")
        print(f"Status: {self.getStatus()}")
        print("=" * 30)
# chỉnh sưa thông tin 
    def edit_StudentID(self, new_student_id):
        query = """
            UPDATE Student
            SET studentID = %s
            WHERE studentID = %s
        """
        main_system.execute_update(
            conn,
            query,
            (new_student_id, self.getStudentID())
        )
        self.setStudentID(new_student_id)
    def edit_Fullname(self, new_fullname):
        query = """
            UPDATE Student
            SET fullName = %s
            WHERE studentID = %s
        """
        main_system.execute_update(
            conn,
            query,
            (new_fullname, self.getStudentID())
        )
        self.setFullname(new_fullname)  
    def edit_Email(self, new_Email):
        query = """
            UPDATE Student
            SET email = %s
            WHERE studentID = %s
        """
        main_system.execute_update(
            conn,
            query,
            (new_Email, self.getStudentID())
        )
        self.setPhone(new_Email)
    def edit_Phone(self, new_phone):
        query = """
            UPDATE Student
            SET phone = %s
            WHERE studentID = %s
        """
        main_system.execute_update(
            conn,
            query,
            (new_phone, self.getStudentID())
        )
        self.setPhone(new_phone)
    def edit_Address(self, new_address):
        query = """
            UPDATE Student
            SET address = %s
            WHERE studentID = %s
        """
        main_system.execute_update(
            conn,
            query,
            (new_address, self.getStudentID())
        )
        self.setAddress(new_address)
    def edit_Idnumber(self, new_idnumber):
        query = """
            UPDATE Student
            SET idNumber = %s
            WHERE studentID = %s
        """
        main_system.execute_update(
            conn,
            query,
            (new_idnumber, self.getStudentID())
        )
        self.setIdnumber(new_idnumber)
    def edit_Status(self, new_status):
        query = """
            UPDATE Student
            SET status = %s
            WHERE studentID = %s
        """
        main_system.execute_update(
            conn,
            query,
            (new_status, self.getStudentID())
        )
        self.setStatus(new_status)
    def edit_info(self, user: User):
    # Xác thực lại user
        if not user.login(user.getUsername(), user.getPassword()):
            print("Xác thực thất bại")
            return

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
            self.edit_StudentID(new_value)

        elif choice == "2":
            new_value = input("Nhập Full name mới: ").strip()
            self.edit_Fullname(new_value)
        elif choice == "3":
            new_value = input("Nhập Email mới: ").strip()
            self.edit_Email(new_value)
        elif choice == "4":
            new_value = input("Nhập Phone mới: ").strip()
            self.edit_Phone(new_value)

        elif choice == "5":
            new_value = input("Nhập Address mới: ").strip()
            self.edit_Address(new_value)

        elif choice == "6":
            new_value = input("Nhập ID number mới: ").strip()
            self.edit_Idnumber(new_value)

        elif choice == "7":
            new_value = input("Nhập Status mới: ").strip()
            self.edit_Status(new_value)

        else:
            print("Lựa chọn không hợp lệ")
            return

        print("Cập nhật thông tin thành công")

    def ViewGrades(self):
        query = """
            SELECT score, grade
            FROM AcademicResult
            WHERE studentID = %s
        """
        grades = main_system.execute_query(conn, query, (self.getStudentID(),))

        if not grades:
            print("Không có dữ liệu điểm")
            return

        for grade in grades:
            print(f"Score : {grade['score']}")
            print(f"Grade : {grade['grade']}")

    def calculateGPA(self):
        query = """
            SELECT 
                s.studentID,
                s.fullName,
                ROUND(
                    SUM(
                        CASE
                            WHEN ar.score >= 8.5 THEN 4.0
                            WHEN ar.score >= 8.0 THEN 3.5
                            WHEN ar.score >= 7.0 THEN 3.0
                            WHEN ar.score >= 6.5 THEN 2.5
                            WHEN ar.score >= 5.5 THEN 2.0
                            WHEN ar.score >= 5.0 THEN 1.5
                            ELSE 0
                        END * c.credit
                    ) / SUM(c.credit)
                , 2) AS GPA_4
            FROM AcademicResult ar
            JOIN Student s ON ar.studentID = s.studentID
            JOIN Class cl ON ar.classID = cl.classID
            JOIN Course c ON cl.courseID = c.courseID
            WHERE s.studentID = %s
            GROUP BY s.studentID, s.fullName
        """

        gpas = main_system.execute_query(conn, query, (self.getStudentID(),))

        if not gpas:
            print("Không có dữ liệu GPA")
            return

        gpa = gpas[0]
        print(f"Student ID : {gpa['studentID']}")
        print(f"Full name  : {gpa['fullName']}")
        print(f"GPA (4.0)  : {gpa['GPA_4']}")

    # hàm join course

    def joinCourse(self, course: Course):
        """
        Sinh viên đăng ký học 1 course (tự động chọn class đang mở)
        """

        # 1. Tìm class của course đang mở enrollment
        query_find_class = """
            SELECT
                c.classID,
                c.maxStudent,
                e.registeredCount,
                e.enrollmentID,
                e.openDate,
                e.endDate
            FROM Class c
            JOIN Enrollment e ON c.classID = e.classID
            WHERE c.courseID = %s
            AND e.openDate <= CURDATE()
            AND e.endDate >= CURDATE()
            LIMIT 1
        """

        rows = main_system.execute_query(
            conn,
            query_find_class,
            (course.get_courseID(),)
        )

        if not rows:
            print("Không có lớp nào đang mở để đăng ký")
            return

        row = rows[0]

        # 2. Kiểm tra sĩ số
        if row["registeredCount"] >= row["maxStudent"]:
            print("Lớp đã đủ sĩ số")
            return

        classID = row["classID"]

        # 3. Kiểm tra sinh viên đã đăng ký chưa
        query_check = """
            SELECT 1
            FROM Enrollment
            WHERE studentID = %s AND classID = %s
        """

        exists = main_system.execute_query(
            conn,
            query_check,
            (self.getStudentID(), classID)
        )

        if exists:
            print("Sinh viên đã đăng ký lớp này")
            return

        # 4. Tạo Enrollment mới
        new_enrollment_id = f"ENR{self.getStudentID()[-3:]}{classID[-3:]}"

        query_insert_enrollment = """
            INSERT INTO Enrollment (
                enrollmentID,
                status,
                openDate,
                endDate,
                registeredCount,
                studentID,
                classID
            )
            VALUES (%s, 'ACTIVE', CURDATE(), CURDATE(), 1, %s, %s)
        """

        success = main_system.execute_update(
            conn,
            query_insert_enrollment,
            (
                new_enrollment_id,
                self.getStudentID(),
                classID
            )
        )

        if not success:
            print("Đăng ký lớp thất bại")
            return

        # 5. Cập nhật sĩ số
        query_update_count = """
            UPDATE Enrollment
            SET registeredCount = registeredCount + 1
            WHERE classID = %s
        """

        main_system.execute_update(conn, query_update_count, (classID,))

        # 6. Tạo AcademicResult rỗng
        query_insert_result = """
            INSERT INTO AcademicResult (
                resultID,
                score,
                grade,
                classID,
                studentID
            )
            VALUES (%s, NULL, NULL, %s, %s)
        """

        result_id = f"RES{self.getStudentID()[-3:]}{classID[-3:]}"

        main_system.execute_update(
            conn,
            query_insert_result,
            (
                result_id,
                classID,
                self.getStudentID()
            )
        )

        print("Đăng ký học phần thành công")
