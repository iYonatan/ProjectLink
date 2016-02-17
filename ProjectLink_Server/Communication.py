from Security import *

import cPickle
import socket
import threading

BUFFER_SIZE = 2048


class ClientSession(threading.Thread):
    def __init__(self, client_conn, client_address):
        super(ClientSession, self).__init__()

        self.pb_key = client_conn.recv(BUFFER_SIZE)
        self.client_sock = client_conn
        self.client_address = client_address

    def run(self):
        sec = Security(public_key=self.pb_key)
        self.client_sock.send(cPickle.dumps(sec.aes_in_pbk))
        print self.client_sock.recv(BUFFER_SIZE)


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
