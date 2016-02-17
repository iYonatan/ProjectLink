from Security import *

import socket
import cPickle

BUFFER_SIZE = 2048


class Communication:
    def __init__(self):

        HOST = 'localhost'  # The remote host
        PORT = 8030  # The same port as used by the server

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((HOST, PORT))
        self.aes_in_pbk = None

    def send(self, data):

        try:
            self.sock.send(data)
            print "The data has been sent to the server"
            return True

        except socket.SO_ERROR:
            print "Couldn't send data to the server"
            return False

    def recv(self):
        return self.sock.recv(BUFFER_SIZE)

    def close(self):
        self.sock.close()

    def run(self):
        sec = Security()
        self.send(sec.export_public_key())

        aes_in_pbk = self.recv()
        self.aes_in_pbk = cPickle.loads(aes_in_pbk)

        sec.decrypt(self.aes_in_pbk)

        comm.close()


comm = Communication()
comm.run()
