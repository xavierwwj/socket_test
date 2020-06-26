"""
Idea of blocking:
With the blocking I/O, when the client makes a connection request to the server, the socket processing 
that connection and the corresponding thread that reads from it is blocked. The context is switched to 
the kernel. The kernel initiates reading - the data is transferred to the user-space buffer. When the
buffer becomes empty, the kernel will wake up the process again to receive the next portion of data 
to be transferred. This data is placed in the network buffer until it is all read and ready for processing.
Until the operation is complete, the server can do nothing more but wait.

Objectives:
    - To test for blocking by the server socket when waiting for connection, and also blocking by the client socket
    when waiting for message
        - To check that when data is sent finish, the next connection is setup, followed by next message
    - To check for error where socket is supposedly closed from client side but from server side the recv method is called
        - print sth inside in case of infinite loop.

Here, Activity Monitor does show 1 thread consistently.
"""

import socket
import time

NUM_CONNECTIONS = 2
CURR_CONNECTION = 0

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 1234))
server_socket.listen(NUM_CONNECTIONS)


while (CURR_CONNECTION<NUM_CONNECTIONS):
    print(time.localtime()) 
    # Add time before and after connection is made. This should show blocking of thread. Indeed it did.
    client_socket, client_address = server_socket.accept() # Here should have blocking until connection request is made
    print(time.localtime())
    messages = []
    firstRecv = True;
    while True:
        data = client_socket.recv(4)
        if firstRecv:
            # Add time after, while adding some pause 
            # to the message in the server side to check for blocking
            # There was blocking 
            print(time.localtime())
            firstRecv = False
        if data:
            messages.append(data)
        else:
            # print(data)
            break 
            # tried to not add a break to check for objective 2. Turned out to be true
            # If closed, recv will keep returning b''
    print(b''.join(messages).decode())
    CURR_CONNECTION +=1