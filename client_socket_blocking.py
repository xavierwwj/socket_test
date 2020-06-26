import socket
import time

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 1234))

message = "testing1234 asdklfnasldfnaslkd"
message2 = "fail"

time.sleep(5)
client_socket.send(message.encode("utf8")) # sending does not close server
time.sleep(1) # added a short pause, and the second send still works, so the socket has not closed
client_socket.send(message2.encode("utf8")) 
# However, reaching the end of the code does close server
# closing server will result in a terminating sequence being sent to the
# other end. The other end uses this info to stop the receiving.

client_socket.close() # just for lols