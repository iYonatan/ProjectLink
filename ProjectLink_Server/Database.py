import mysql.connector


class Connector:
    def __init__(self):

        self.user = 'project_link'
        self.password = 'yonatan135'
        self.hostname = 'db4free.net'
        self.database_name = 'yonatan_eilat'

        self.Username = None
        self.user_id = None
        self.computer_id = None

    def connect(self):
        self.cnx = mysql.connector.connect(user=self.user,
                                           password=self.password,
                                           host=self.hostname,
                                           database=self.database_name)
        if self.cnx.is_connected():
            print "DB is connected\n--------------\n"

    def execute(self, query, args, commit=False):
        cursor = self.cnx.cursor()
        cursor.execute(query, args)
        if commit:
            self.cnx.commit()
            return
        return cursor.fetchall()

    def find_user_id(self):
        query = "SELECT User_ID FROM users WHERE Username = %s"
        args = (self.Username,)
        return self.execute(query, args)[0][0]  # user_id

    def user_exists(self, user_password):
        # TODO: Needs to check the password too

        query = "SELECT Username FROM users WHERE Username = %s AND Password = %s"
        args = (self.Username, user_password)
        if not self.execute(query, args):
            print "The username does not exist"
            return False
        else:
            print "{} exists".format(self.Username)
            return True

    def computer_exists(self):
        query = "SELECT Computer_ID FROM computer WHERE User_ID = %s  AND Computer_ID = %s"
        args = (self.user_id, self.computer_id)
        results = self.execute(query, args)
        print results
        return results

    def add_computer(self, OS_version, CPU_model, CPU_num, Memo_Total_Ram):
        query = """INSERT INTO computer (User_ID, Computer_ID, OS_version)
                                        VALUES (%s, %s, %s)"""
        args = (self.user_id, self.computer_id, OS_version)
        self.execute(query, args, True)

        query = """INSERT INTO system (User_ID, Computer_ID, CPU_model, CPU_num, Memo_Total_Ram)
                                        VALUES (%s, %s, %s, %s, %s)"""
        args = (self.user_id, self.computer_id, CPU_model, CPU_num, Memo_Total_Ram)
        self.execute(query, args, True)

        query = """INSERT INTO events (User_ID, Computer_ID) VALUES (%s, %s)"""
        args = (self.user_id, self.computer_id)
        self.execute(query, args, True)

        print "New Computer has been added"
        return

    def update_query(self, data_list):
        table_name = data_list[0]
        column_name = data_list[1]
        value = data_list[2]

        query = "UPDATE {} SET {} = {} WHERE  User_ID = {} AND Computer_ID = '{}'".format(
            table_name, column_name, value, self.user_id, self.computer_id)

        self.execute(query, (), True)

        # print "Some data has been added to the database"

# Username = 'iYonatan'
# c = Connector(Username)
#
# query = "INSERT INTO users (Username, Password, Email, First_name, Last_name, Computer_num)\
# VALUES (%s, %s, %s, %s, %s, %s)"
# args = ("GG", "golden", "guy11053@gmail.com", "Guy", "Gold", 0)
#
# c.execute(query, args)
