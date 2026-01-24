from Main_System import main_system
from datetime import date
from Class.Student import Student
conn = main_system.connect_db()
class Class:
    def __init__(self,classId):
        query = """
            SELECT
                classID,
                schedule,
                maxStudent,
                courseID,
                instructorID,
                roomID
            FROM Class
            WHERE classID = %s
        """

        rows = main_system.execute_query(
            conn,
            query,
            (classId,)
        )

        if not rows:
            raise ValueError("Không tìm thấy class")

        row = rows[0]  # row là dict

        self.__classID= row["classID"]
        self.__schedule= row["schedule"]
        self.__maxStudent= row["maxStudent"]
        self.__courseID= row["courseID"]
        self.__instructorID= row["instructorID"]
        self.__roomID = row["roomID"]
        
        # viết hàm getter và setter cho tất cả thuộc tính
    def getClassID(self):
        return self.__classID
    def setClassID(self, classID):
        self.__classID = classID
    def getSchedule(self):
        return self.__schedule
    def setSchedule(self, schedule):
        self.__schedule = schedule
    def getMaxStudent(self):
        return self.__maxStudent
    def setMaxStudent(self, maxStudent):
        self.__maxStudent = maxStudent
    def getCourseID(self):
        return self.__courseID
    def setCourseID(self, courseID):
        self.__courseID = courseID
    def getInstructorID(self):
        return self.__instructorID
    def setInstructorID(self, instructorID):
        self.__instructorID = instructorID
    def getRoomID(self):
        return self.__roomID
    def setRoomID(self, roomID):
        self.__roomID = roomID