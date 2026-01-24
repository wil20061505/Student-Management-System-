from Main_System import main_system
conn = main_system.connect_db()
class AcademicResult:
    def __init__(self, resultID):
        query = """
            SELECT
                resultID,
                score,
                grade,
                classID,
                studentID
            FROM AcademicResult
            WHERE resultID = %s
        """

        rows = main_system.execute_query(
            conn,
            query,
            (resultID,)
        )

        if not rows:
            raise ValueError("Không tìm thấy AcademicResult")

        row = rows[0]

        self.__resultID = row["resultID"]
        self.__score = row["score"]
        self.__grade = row["grade"]
        self.__classID = row["classID"]
        self.__studentID = row["studentID"]

    # getter
    def getResultID(self):
        return self.__resultID

    def getScore(self):
        return self.__score

    def getGrade(self):
        return self.__grade

    def getClassID(self):
        return self.__classID

    def getStudentID(self):
        return self.__studentID
    
    # setter
    def setScore(self, score):
        if score < 0 or score > 10:
            raise ValueError("Điểm phải nằm trong khoảng 0–10")
        self.__score = score
        self.__grade = self.__calculateGrade(score)

    def setGrade(self, grade):
        self.__grade = grade

    def setClassID(self, classID):
        self.__classID = classID

    def setStudentID(self, studentID):
        self.__studentID = studentID

    def __calculateGrade(self, score):
        if score >= 8.5:
            return 'A'
        elif score >= 7.0:
            return 'B'
        elif score >= 5.5:
            return 'C'
        else:
            return 'D'
