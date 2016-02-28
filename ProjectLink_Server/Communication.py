import socket
import threading
import time
import cPickle

from Security import *

BUFFER_SIZE = 2048


class ClientSession(threading.Thread):
    def __init__(self, client_conn, client_address, db_conn):
        super(ClientSession, self).__init__()

        self.db_conn = db_conn
        self.client_sock = client_conn
        self.client_address = client_address
        self.sec = Security()

    def send(self, data):
        try:
            self.client_sock.send(cPickle.dumps(self.sec.encrypt(cPickle.dumps(data))))
            # self.client_sock.send(data)
            print "{} - has been sent to the server".format(data)
            return True

        except socket.SO_ERROR:
            print "Couldn't send data to the server"
            return False

    def recv(self):
        # return self.sec.decrypt(cPickle.load(self.client_sock.recv(BUFFER_SIZE)))
        return cPickle.loads(self.sec.decrypt(cPickle.loads(self.client_sock.recv(BUFFER_SIZE))))

    def run(self):

        self.client_sock.send(self.sec.export_public_key())
        self.sec.client_public_key = Security.import_key(self.client_sock.recv(1024))
        (self.sec.aes_key, self.sec.mode, self.sec.iv) = cPickle.loads(self.client_sock.recv(1024))
        self.sec.create_cipher()

        user_data = self.recv()
        print user_data

        # -- Checking if the user exists in the database -- #
        USERNAME = user_data[0]
        PASSWORD = user_data[1]

        self.db_conn.Username = USERNAME
        self.db_conn.user_id = self.db_conn.find_user_id()
        # -- ------------------------------------------- -- #

        if not self.db_conn.user_exists(PASSWORD):
            self.send('400 NOT FOUND')
            return
        self.send('200 OK')  # If the user exists

        UUID = self.recv()
        self.db_conn.computer_id = UUID[2]
        print UUID

        # -- Checking if the computer's UUID exists in the database -- #

        if not self.db_conn.computer_exists():
            self.send('400 NOT FOUND')
            os_version = self.recv()[2]
            print os_version

            cpu_model = self.recv()[2]
            print cpu_model

            cpu_num = self.recv()[2]
            print cpu_num

            memo_total_ram = self.recv()[2]
            print memo_total_ram

            self.db_conn.add_computer(os_version, cpu_model, cpu_num, memo_total_ram)
            print "Computer has been added"
        else:
            self.send('200 OK')
        # -- ------------------------------------------- -- #

        while True:
            data = self.recv()
            if type(data) is list:
                self.db_conn.update_query(data)
            time.sleep(1)


class Communication:
    def __init__(self, db_conn):
        self.db_conn = db_conn

        self.open_clients = []
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(('', 8030))
        self.sock.listen(5)
        print "Waiting for connections...\n\n"

    def send(self, data):
        try:
            self.sock.send(data)
            print "The data has been sent to the server"

        except socket.SO_ERROR:
            print "Couldn't send data to the server"

    def recv(self):
        return self.sock.recv(BUFFER_SIZE)

    def close(self):
        self.sock.close()

    def run(self):
        (client_conn, client_address) = self.sock.accept()
        if client_address[0] in self.open_clients:
            client_session = ClientSession(client_conn, client_address, self.db_conn)
            client_session.run()
        else:
            self.open_clients.append(client_address[0])
            client_session = ClientSession(client_conn, client_address, self.db_conn)
            client_session.run()
