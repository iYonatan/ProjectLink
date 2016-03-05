import cPickle
import json
import socket
from Security import *

BUFFER_SIZE = 2048


class Communication:
    def __init__(self):

        HOST = 'localhost'  # The remote host
        PORT = 8030  # The same port as used by the server

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((HOST, PORT))

        self.sec = Security()

    def send(self, data):
        self.sock.settimeout(1)
        try:
            self.sock.send(self.sec.encrypt(json.dumps(data)))
            return True

        except socket.SO_ERROR:
            print "Couldn't send data: %s to the server" % data
            return False

    def recv(self):
        temp_data = self.sock.recv(BUFFER_SIZE)
        data = ""
        self.sock.settimeout(0.5)

        while len(temp_data) > 0:

            data += temp_data
            try:
                temp_data = self.sock.recv(BUFFER_SIZE)
            except:
                break
        self.sock.settimeout(5)

        return cPickle.loads(self.sec.decrypt(data))

    def close(self):
        self.sock.close()
