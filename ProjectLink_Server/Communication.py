import socket
import threading

BUFFER_SIZE = 2048


class Communication:
    def __init__(self):

        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.bind(('', 8030))
            self.sock.listen(5)

        except socket.SO_ERROR:
            print "Couldn't create the sever"

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
