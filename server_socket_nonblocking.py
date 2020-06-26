import socket
import time
import select

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setblocking(0) # non-blocking for server socket
server_socket.bind(('localhost', 1234))
server_socket.listen(5) # if we try to accept more than this, there will be ConnectionRefusedError
# Note: the moment we apply this listen() method is when
# the socket can no longer act like a client socket but 
# functions as a passive socket to create other sockets
print('Server started at')
print(time.localtime())
print('')

socket_in = [server_socket]
socket_out = []
# print(server_socket) This does work
while socket_in:
    """
    Purpose of select: to check for readiness so that any
    following calls that may usually need blocking are guaranteed
    to not need them, thus allowing us to use nonblocking mode.
    For sockets, readiness comes in different forms i.e. one
    of the following.
    """
    """
    A socket becomes ready for reading when someone connects 
    after a call to listen (which means that accept won’t
    block), when data arrives from the remote end, or when 
    the socket is closed or reset (in this case, recv will 
    return an empty string).

    A socket becomes ready for writing when the connection 
    is established after a non-blocking call to connect or 
    when data can be written to the socket.

    A socket signals an error condition when the connection 
    fails after a non-blocking call to connect.

    The optional timeout argument specifies a time-out as a 
    floating point number in seconds. When the timeout 
    argument is omitted the function blocks until at least 
    one file descriptor is ready.
    """
    readable, writable, exceptional = select.select(socket_in, socket_out, socket_in)
    print(time.localtime()) 
    """
    This will be the time at which the connection request
    was sent. Prior to that, select was blocking the thread
    as the socket was not ready to be read. Only when 
    connection request is here, is the socket deemed ready
    i.e. guaranteed to not need blocking.

    Commenting the entire chunk below will result in the
    loop printing the time infinitely, because the socket
    is ready after the first connection, but accept was
    not run yet.
    """
    for s in readable:
        if s is server_socket:
            print("server socket")
            client_socket, client_address = s.accept() 
            #client_socket.setblocking(0)
            """
            Now we can perform accepting without a need for blocking.
            Only after accepting, does blocking become needed,
            and so the server socket becomes not ready. 
            """
            socket_in.append(client_socket)
            # client socket should still remain blocked.
            # Does not matter actually, because if data is
            # not here, the select will know that it is not
            # ready. Even for experiment 2.
        else:
            print("client socket")
            data = s.recv(1024)
            if data:
                print(data)
            else:
                socket_in.remove(s)
                s.close()
                print("close")
    time.sleep(5)
    """
    Doing this and then running this file, followed by two
    separate client connections (to allow us to turn on the
    second client) will give the following result:

    1) select returns when first connection request was sent
    2) server socket is now ready and server side accepts without blocking
    3) sleep 5 seconds (by now we shd have manually turned on 2nd connection)
    4) now both server socket and the first client socket are ready
    5) server socket accepts 2nd connection readily
    6) client's first socket prints message
    7) sleep
    8) server socket is now not ready coz no new connection
    9) first client socket is ready, receives 0 bytes, closes
    10) second client receives message
    11) sleep
    12) server socket not ready, 1st client closed, left 2nd client
    13) 2nd clint receives 0 bytes and close
    14) sleep and await new connections
    """

"""
Experiment 2: 
    add time.sleep(7.5) to client socket, 
    then spam run both connections, with nonblocking 
    for client
Result:
    1) connection 1 is made first
    2) timeout 5s.
    3) because of the timeout 7.5s, the message is not ready
    4) connection 2 is then made first after the 5s timeout on server side
    5) finally connection 1's message is sent after 2.5s
    6) connection 2's message is sent also slightly after
    7) meanwhile there is 5s timeout, where 2.5s remains
    5) receive both messages together
    6) close, close together
"""