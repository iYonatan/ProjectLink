import mysql.connector


class Connector:
    def __init__(self):
        self.user = 'root'
        self.password = 'yonataneilat135'
        self.hostname = 'localhost'
        self.database_name = 'sys'

        self.__connect()

    def __connect(self):
        self.cnx = mysql.connector.connect(user=self.user,
                                           password=self.password,
                                           host=self.hostname,
                                           database=self.database_name)
        if self.cnx.is_connected():
            print "DB is connected"

    def execute(self, query, args):
        cursor = self.cnx.cursor()
        cursor.execute("SELECT * FROM users WHERE User-ID = %s" % 6)
        print cursor.fetchall()


c = Connector()

query = "INSERT INTO users (Username, Password, Email, First_name, Last_name, Computer_num)\
VALUES (%s, %s, %s, %s, %s, %s)"
args = ("GG", "golden", "guy11053@gmail.com", "Guy", "Gold", 0)

c.execute(query, args)
