import socket
import time

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 1234))

message = "testing1234 asdklfnasldfnaslkd"

time.sleep(7.5)
client_socket.send(message.encode("utf8"))
# time.sleep(10)
# client_socket.send("test".encode("utf8"))

client_socket.close() # just for lols