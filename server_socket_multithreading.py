import socket
import time
import threading
import concurrent.futures

NUM_OF_THREADS = 3
CURR_NUM = 0

def client_func(sock, thread_no):
    message = []
    while True:
        data = sock.recv(16)
        if data:
            print("From thread "+str(thread_no)+": "+data.decode("utf8"))
            message.append(data)
        else:
            break
        time.sleep(1)
    print(b''.join(message).decode("utf8"))
    """
    Without any timeout here, there is no blocking, so the
    moment each thread is spawned, this whole thing is run.

    If we added timeout, we will see all the subthreads running,
    as well as the main thread still picking up new connections.
    """

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 1234))
server_socket.listen(NUM_OF_THREADS)
print("Server is listening")

with concurrent.futures.ThreadPoolExecutor(max_workers = NUM_OF_THREADS) as executor:
    while (CURR_NUM < NUM_OF_THREADS):
        client_socket, client_address = server_socket.accept() # This blocks until a new connection
        print("Time for connection "+str(CURR_NUM+1)+":")
        print(time.localtime())
        executor.submit(client_func, client_socket, CURR_NUM+1) 
        # Upon receiving connection, a new child thread should spawn and run while the main thread awaits new connection
        CURR_NUM += 1
    """
    Using with will create a ThreadPoolExecutor, followed by automatically closing it when the block is
    completed. In the context of this object, closing will include the act of joining threads, whether they
    are non-daemon or not.
    """


"""
Experiment:
    - Set up threads of client sockets in blocking mode with timeout

"""