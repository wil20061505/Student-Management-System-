from Main_System import main
conn = main.connect_db()
class classRoom:
    def __init__(self,roomID):
        query = """
            SELECT
    roomID ,
    roomName,
    capacity
            FROM ClassRoom
            WHERE roomID = %s
        """

        rows = main.execute_query(
            conn,
            query,
            (roomID,)
        )

        if not rows:
            raise ValueError("Không tìm thấy lớp học ")

        row = rows[0]  # row là dict
        self.__roomID = row["roomID"]
        self.__roomName  = row["roomName"]
        self.__capacity = row["capacity"]

    # Getters
    def get_roomID(self):
        return self.__roomID
    
    def get_roomName(self):
        return self.__roomName
    
    def get_capacity(self):
        return self.__capacity
    
    # Setters
    def set_roomName(self, roomName):
        self.__roomName = roomName
    
    def set_capacity(self, capacity):
        self.__capacity = capacity
