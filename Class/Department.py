from Main_System import main_system
conn = main_system.connect_db()
class Department:
    def __init__(self, departmentID):
        query = """
            SELECT
                departmentID,
                departmentName
            FROM Department
            WHERE departmentID = %s
        """

        rows = main_system.execute_query(
            conn,
            query,
            (departmentID,)
        )

        if not rows:
            raise ValueError("Không tìm thấy Department")

        row = rows[0]

        self.__departmentID = row["departmentID"]
        self.__departmentName = row["departmentName"]

    # Getter
    def getDepartmentID(self):
        return self.__departmentID

    def getDepartmentName(self):
        return self.__departmentName

    # Setter
    def setDepartmentName(self, name: str):
        self.__departmentName = name
