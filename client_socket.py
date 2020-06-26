import socket

"""
socket.socket(ADDRESS_FAMILY, SOCKET TYPE)
    - ADDRESS_FAMILY defines the OSI netowkr layer protocol to use
    - SOCKET_TYPE defines the OSI transport layer protocol to use
    - SOCK_DGRAM is UDP, SOCK_STREAM is TCP.
    - INET is IPv4, INET is IPv6
"""

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
s.connect(("www.w3.org", 80));

"""
To request a response from the server, there are mainly two methods:
    - GET: to request data from the server.
    - POST: to submit data to be processed to the server.

"""
s.send("GET https://www.w3.org/TR/PNG/iso_8859-1.txt HTTP/1.1\nHost: www.w3.org\n\n".encode("utf8")); 
"""
- Messages need to be encoded
- HTTP 1.1 needs a host header. Sometimes HTTP 1.0 needs as well.
""" 

counter = 0;
while True:
    """
    Here we define the buffer size for receiving from the network buffer. Typically, when we send or receive, data gets pushed
    to or taken from the network buffer. You need to continuously call to get the entire data. Once 0 bytes is received, 
    """
    data = s.recv(1024); 
    if data == b'': # Here we can also check if len(string) < 1
        break; # If we reach this point, the socket gets broken!!
        """
        But if you plan to reuse your socket for further transfers, you need to realize that there is no EOT on a socket. 
        I repeat: if a socket send or recv returns after handling 0 bytes, the connection has been broken. If the connection 
        has not been broken, you may wait on a recv forever, because the socket will not tell you that there’s nothing more 
        to read (for now). Now if you think about that a bit, you’ll come to realize a fundamental truth of sockets: messages 
        must either be fixed length (yuck), or be delimited (shrug), or indicate how long they are (much better), or end by 
        shutting down the connection. The choice is entirely yours, (but some ways are righter than others).
        """
    print(data.decode("utf8"));
    counter += 1;

print(counter);

s.close();