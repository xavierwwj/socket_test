import socket

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

clientsocket.connect(("192.168.86.143", 1234))

MSGLEN = 21;
NUMBER_OF_MSGS = 5
C = 0

while(NUMBER_OF_MSGS > C): 
    # Allows for multiple messages to be sent in one connection, as long as we track message length and do not send 0 bytes
    # Here we assume knowledge of the message length, however, we can also check message length through the first byte of any message data
    totalrecv = 0
    data = []
    while totalrecv < MSGLEN:
        sub_data = clientsocket.recv(min(2, MSGLEN-totalrecv))
        totalrecv += len(sub_data)
        data.append(sub_data)
        if len(sub_data) == 0:
            print("socket connection broken from recv side")
            # This means that the server sent a 0 byte file, which means that the socket was automatically closed from their side
            break
    print(b''.join(data).decode("utf8"))
    C += 1;

clientsocket.close(); 
# We close the socket when done to prevent the other party from waiting for something that will not come.
# E.g. they actually want to send multiple messages but we just want one message. We close it, and this nullifies the buffers for 
# both sides as well as the socket entirely.