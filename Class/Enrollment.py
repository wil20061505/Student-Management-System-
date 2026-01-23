from Main_System import main
conn = main.connect_db()
from datetime import date

class Enrollment:
    def __init__(self, classID, studentID):
        query = """
            SELECT
                enrollmentID,
                status,
                openDate,
                endDate,
                registeredCount,
                studentID,
                classID
            FROM Enrollment
            WHERE classID = %s
              AND studentID = %s
        """

        rows = main.execute_query(
            conn,
            query,
            (classID, studentID)
        )

        if not rows:
            raise ValueError("Không tìm thấy thông tin đăng ký lớp")

        row = rows[0]  # dict

        self.__enrollmentID = row["enrollmentID"]
        self.__status = row["status"]
        self.__openDate = row["openDate"]
        self.__endDate = row["endDate"]
        self.__registeredCount = row["registeredCount"]
        self.__studentID = row["studentID"]
        self.__classID = row["classID"]

    def getEnrollmentID(self):
        return self.__enrollmentID

    def getStatus(self):
        return self.__status

    def getOpenDate(self):
        return self.__openDate

    def getEndDate(self):
        return self.__endDate

    def getRegisteredCount(self):
        return self.__registeredCount

    def getStudentID(self):
        return self.__studentID

    def getClassID(self):
        return self.__classID
    
    def setStatus(self, status: str):
        self.__status = status

    def setOpenDate(self, openDate: date):
        self.__openDate = openDate

    def setEndDate(self, endDate: date):
        self.__endDate = endDate

    def setRegisteredCount(self, count: int):
        if count < 0:
            raise ValueError("registeredCount không được âm")
        self.__registeredCount = count

    def setStudentID(self, studentID: str):
        self.__studentID = studentID

    def setClassID(self, classID: str):
        self.__classID = classID

    def isOpen(self) -> bool:
        today = date.today()
        return self.__openDate <= today <= self.__endDate
    def increaseRegisteredCount(self):
        self.__registeredCount += 1
