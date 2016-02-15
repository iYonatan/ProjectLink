import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('', 8030))
sock.listen(1)

conn, addr = sock.accept()
print "Client: {}".format(addr)

client_data = conn.recv(2048)
print client_data
