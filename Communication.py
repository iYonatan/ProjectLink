import socket


class Communication:
    def __init__(self):

        self.BUFFER_SIZE = 2048
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def protocol_steps(self, UUID):
        try:
            self.sock.connect(('192.168.1.12', 8030))

        except socket.SO_ERROR:
            print "Couldn't connect to the server"

        server_response = self.recv()
        if server_response != "200 OK":
            raise socket.SO_ERROR("Protocol error: Couldn't connect to the server")

        print "Connected to the server !"

        """
         Here the client needs to send to the server the username and the password
        """

        if not self.send(UUID):
            raise Exception("UUID was not sent")

        print "Protocols steps successfuly worked"

    def send(self, data):

        try:
            self.sock.send(data)
            print "The data has been sent to the server"
            return True

        except socket.SO_ERROR:
            print "Couldn't send data to the server"
            return False

    def recv(self):
        return self.sock.recv(self.BUFFER_SIZE)
