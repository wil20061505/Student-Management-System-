from Main_System import main
conn = main.connect_db()
class User:
    #hàm tạo 
    def __init__(self,userId,username,password,role):
        
        self.__userId = userId
        self.__username = username
        self.__password = password
        self.__role = role
    
    # Getter và Setter cho userId
    def getUserId(self):
        return self.__userId
    
    def setUserId(self, userId):
        self.__userId = userId
    
    # Getter và Setter cho username
    def getUsername(self):
        return self.__username
    
    def setUsername(self, username):
        self.__username = username
    
    # Getter và Setter cho password
    def getPassword(self):
        return self.__password
    
    def setPassword(self, password):
        self.__password = password
    
    # Getter và Setter cho role
    def getRole(self):
        return self.__role
    
    def setRole(self, role):
        self.__role = role
    
    # hàm phương thức
    def login(self, username, password):
        query = """
        SELECT userId, userName, password, role
        FROM User
        WHERE userName = %s AND password = %s
    """
        rows = main.execute_query(conn, query, (username, password))
        if not rows:
            return False
        row = rows[0]  # row là dict
        self.setUserId(row["userId"])
        self.setUsername(row["userName"])
        self.setPassword(row["password"])
        self.setRole(row["role"])
        return True



    def logout(self):
        self.setUserId(None)
        self.setUsername(None)
        self.setPassword(None)
        self.setRole(None)
        return True



    def change_passWord(self, username, password,Newpassword):
        if self.login(username, password):
            self.setPassword(Newpassword)
            return True
        return False