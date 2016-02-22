import cPickle
import socket
import threading
import time

from Database import Connector
from Security import *

BUFFER_SIZE = 2048


class ClientSession(threading.Thread):
    def __init__(self, client_conn, client_address):
        super(ClientSession, self).__init__()

        self.db_conn = None
        self.client_sock = client_conn
        self.client_address = client_address
        self.sec = Security()

    def send(self, data):
        try:
            # self.sock.send(cPickle.dumps(self.sec.encrypt(data)))
            self.client_sock.send(data)
            print "The data has been sent to the server"
            return True

        except socket.SO_ERROR:
            print "Couldn't send data to the server"
            return False

    def recv(self):
        # return self.sec.decrypt(self.client_sock.recv(BUFFER_SIZE))
        return cPickle.loads(self.client_sock.recv(BUFFER_SIZE))

    def run(self):
        self.send(self.sec.export_public_key())
        user_data = self.recv()
        print user_data

        # -- Checking if the user exists in the database -- #
        USERNAME = user_data.split('|')[0]
        PASSWORD = user_data.split('|')[1]
        self.db_conn = Connector(USERNAME)

        # -- ------------------------------------------- -- #
        if not self.db_conn.user_exists(PASSWORD):
            self.send('400 NOT FOUND')
            return
        self.send('200 OK')  # If the user exists

        UUID = self.recv()
        self.db_conn.computer_id = UUID
        print UUID

        # -- Checking if the computer's UUID exists in the database -- #
        if not self.db_conn.computer_exists():
            self.send('400 NOT FOUND')
            os_version = self.recv()
            print os_version

            cpu_model = self.recv()
            print cpu_model

            cpu_num = self.recv()
            print cpu_num

            memo_total_ram = self.recv()
            print memo_total_ram

            self.db_conn.add_computer(os_version, cpu_model, cpu_num, memo_total_ram)
            print "Computer has been added"
        else:
            self.send('200 OK')
        # -- ------------------------------------------- -- #

        while True:
            print self.recv()
            time.sleep(1)


class Communication:
    def __init__(self):
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
            client_session = ClientSession(client_conn, client_address)
            client_session.run()
        else:
            self.open_clients.append(client_address[0])
            client_session = ClientSession(client_conn, client_address)
            client_session.run()
