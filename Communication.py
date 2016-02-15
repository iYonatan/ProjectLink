from Security import *
import socket

BUFFER_SIZE = 2048


class Communication:
    def __init__(self):

        HOST = 'localhost'  # The remote host
        PORT = 8030  # The same port as used by the server

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((HOST, PORT))

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
        comm.close()


comm = Communication()
comm.run()