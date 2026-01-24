from Main_System import main_system
conn = main_system.connect_db()
class Instructor:
    def __init__(self, instructorID):
        query = """
            SELECT
                instructorID,
                fullName,
                email
            FROM Instructor
            WHERE instructorID = %s
        """

        rows = main_system.execute_query(
            conn,
            query,
            (instructorID,)
        )

        if not rows:
            raise ValueError("Không tìm thấy Instructor")

        row = rows[0]

        self.__instructorID = row["instructorID"]
        self.__fullName = row["fullName"]
        self.__email = row["email"]

    # Getter
    def getInstructorID(self):
        return self.__instructorID

    def getFullName(self):
        return self.__fullName

    def getEmail(self):
        return self.__email

    # Setter
    def setFullName(self, name: str):
        self.__fullName = name

    def setEmail(self, email: str):
        self.__email = email
