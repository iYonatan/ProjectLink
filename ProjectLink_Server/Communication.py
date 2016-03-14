import socket
import threading
import time
import cPickle
import json

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
            self.client_sock.send(self.sec.encrypt(json.dumps(data)))
            print "{} - has been sent to the client".format(data)
            return True

        except socket.SO_ERROR:
            print "Couldn't send data to the server"
            return False

    def recv(self, timeout=True):
        temp_data = self.client_sock.recv(BUFFER_SIZE)

        if timeout:
            self.client_sock.settimeout(5)

        decrypted_data = self.sec.decrypt(temp_data)
        try:
            return json.loads(decrypted_data)

        except Exception as e:
            print e
            return

    def user_handle(self):
        user_data = self.recv(False)
        print user_data

        # -- Checking if the user exists in the database -- #
        USERNAME = user_data[0]
        PASSWORD = user_data[1]

        if not self.db_conn.user_exists(USERNAME, PASSWORD):
            self.send('400 NOT FOUND')
            return self.user_handle()

        return USERNAME, PASSWORD

    def run(self):
        self.client_sock.send(self.sec.export_public_key())
        (self.sec.aes_key, self.sec.mode, self.sec.iv) = cPickle.loads(self.client_sock.recv(1024))
        self.sec.create_cipher()

        (USERNAME, PASSWORD) = self.user_handle()
        # -- ------------------------------------------- -- #

        self.db_conn.Username = USERNAME
        print self.db_conn.Username
        self.db_conn.user_id = self.db_conn.find_user_id()
        self.send('200 OK')  # If the user exists

        UUID = self.recv()[2]
        self.db_conn.computer_id = UUID

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
            print data
            if type(data) is list:
                self.db_conn.update_query(data)


class Communication:
    def __init__(self, db_conn):
        self.db_conn = db_conn

        self.open_clients = []
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(('0.0.0.0', 8030))
        self.sock.listen(5)
        print "Waiting for connections...\n\n"

    def send(self, data):
        try:
            self.sock.send(data)
            print "The data has been sent to the client"

        except socket.SO_ERROR:
            print "Couldn't send data to the server"

    def recv(self):
        return self.sock.recv(BUFFER_SIZE)

    def close(self):
        self.sock.close()

    def run(self):
        (client_conn, client_address) = self.sock.accept()
        print client_address
        if client_address[0] in self.open_clients:
            client_session = ClientSession(client_conn, client_address, self.db_conn)
            client_session.run()
        else:
            self.open_clients.append(client_address[0])
            client_session = ClientSession(client_conn, client_address, self.db_conn)
            client_session.run()
