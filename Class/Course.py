from Main_System import main
conn = main.connect_db()
class Course:
    def __init__(self,CourseID):
        query = """
            SELECT
                courseID,
    courseCode ,
    courseName ,
    credit,
    departmentID
            FROM Course
            WHERE CourseID = %s
        """

        rows = main.execute_query(
            conn,
            query,
            (CourseID,)
        )

        if not rows:
            raise ValueError("Không tìm thấy khóa học ")

        row = rows[0]  # row là dict
        self.__courseID = row["courseID"]
        self.__courseCode  = row["courseCode "]
        self.__courseName = row["courseName"]
        self.__credit = row["credit"]
        self.__departmentID = row["departmentID"]

    # Getters
    def get_courseID(self):
        return self.__courseID
    
    def get_courseCode(self):
        return self.__courseCode
    
    def get_courseName(self):
        return self.__courseName
    
    def get_credit(self):
        return self.__credit
    
    def get_departmentID(self):
        return self.__departmentID
    
    # Setters
    def set_courseCode(self, courseCode):
        self.__courseCode = courseCode
    
    def set_courseName(self, courseName):
        self.__courseName = courseName
    
    def set_credit(self, credit):
        self.__credit = credit
    
    def set_departmentID(self, departmentID):
        self.__departmentID = departmentID
    