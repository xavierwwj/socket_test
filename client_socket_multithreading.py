import socket
import time

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 1234))

message = "In this post, we will be talking about networking but you can easily map it to other input/output(I/O) operations, for example, change sockets to file descriptors. Also, this explanation is not focusing on any specific programming language although the examples will be given in Python(what can I say – I love Python!)."

client_socket.send(message.encode("utf8"))


client_socket.close()