import cPickle
import socket
import threading

import time

from Security import *

BUFFER_SIZE = 2048


class ClientSession(threading.Thread):
    def __init__(self, client_conn, client_address):
        super(ClientSession, self).__init__()
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
        return self.client_sock.recv(BUFFER_SIZE)

    def run(self):
        self.client_sock.send(self.sec.export_public_key())
        user_data = self.recv()
        print user_data

        # -- Checking if the user exists in the database -- #

        # -- ------------------------------------------- -- #

        self.send('200 OK')  # If the user exists

        UUID = self.recv()
        print UUID
        # -- Checking if the computer's UUID exists in the database -- #

        # -- ------------------------------------------- -- #
        while True:
            print self.recv()
            time.sleep(3)


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
