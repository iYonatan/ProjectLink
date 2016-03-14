import cPickle
import json
import socket

from Security import *

BUFFER_SIZE = 2048  # send / recive buffer size


class Communication:
    def __init__(self):

        HOST = 'localhost'  # IP host
        PORT = 8030  # The same port as used by the server

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create socket object
        self.sock.connect((HOST, PORT))  # socket connects to the server

        self.sec = Security()  # Creates Security instance (object)

    def send(self, data):
        """
        Sends encrypted data to the server
        :param data: client data (string)
        :return: If data has been sent or if hasn't (boolean)
        """
        try:
            self.sock.send(self.sec.encrypt(json.dumps(data)))  # Sends cncrypted data to the server
            return True  # Returns if the data has been sent

        except socket.SO_ERROR:
            print "Couldn't send data: %s to the server" % data
            return False

    def recv(self, timeout=True):
        """
        Recives encrypted data from the server
        :param timeout: If the client needs timeout (True for default)
        :return: encrypted data (string)
        """
        temp_data = self.sock.recv(BUFFER_SIZE)

        if timeout:
            self.sock.settimeout(5)

        decrypted_data = self.sec.decrypt(temp_data)
        try:
            return json.loads(decrypted_data)

        except Exception as e:
            print e
            return

    def close(self):
        self.sock.close()
