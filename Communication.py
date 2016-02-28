import cPickle
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
        try:
            self.sock.send(cPickle.dumps(self.sec.encrypt(cPickle.dumps(data))))
            return True

        except socket.SO_ERROR:
            print "Couldn't send data: %s to the server" % data
            return False

    def create_symetric_key(self):
        pass

    def recv(self):
        return cPickle.loads(self.sec.decrypt(cPickle.loads(self.sock.recv(BUFFER_SIZE))))

    def close(self):
        self.sock.close()

    def run(self):
        pass
