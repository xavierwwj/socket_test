"""
A Lock is an object that acts like a hall pass. Only one thread at a time can have the Lock. 
Any other thread that wants the Lock must wait until the owner of the Lock gives it up.

The basic functions to do this are .acquire() and .release(). A thread will call my_lock.acquire() 
to get the lock. If the lock is already held, the calling thread will wait until it is released. 
There’s an important point here. If one thread gets the lock but never gives it back, your program 
will be stuck. You’ll read more about this later.

Fortunately, Python’s Lock will also operate as a context manager, so you can use it in a with 
statement, and it gets released automatically when the with block exits for any reason.

Basically spawning lockless threads will allow the system to process various threads all together,
while threads with locking allow the system to perform blocking at the point of lock acquiring if
lock is already held.

Applications:
    - Beating race conditions and creating a deterministic flow / result
    - Control a sequence of events (process synchronisation) when there is presence of asynchronous 
    events (like data transfer)

Note:
if a thread cannot acquire lock, it is blocked, but even then
this does not mean it will have priority after the lock is
released
"""
import socket
import time
import threading

no_defects = True
buffer1 = 0
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 1234))
server_socket.listen(5)
def_lock = threading.Lock()
buffer_lock = threading.Lock()

def thread1_func(server_socket, def_lock, buffer_lock):
    # while True:
    #   listen(CCD) # This is a blocking call
    #   add_waveforms(LUT, buffer1) # Another lock needs to be added again
    #   with state_lock:
    #       global no_defects
    #       no_defects = false
    
    while True:
        # Here we add a sample blocking call that functions similarly
        # we add a socket connection listener
        client_socket, client_address = server_socket.accept()
        
        # To add the waveforms part
        global buffer1
        with buffer_lock:
            buffer1 = 1
            print("Buffer ready")

        with def_lock:
            global no_defects
            no_defects = False

        # Issue with above code is that before first buffer
        # is sent, the second buffer came and replaced it.
        # This may not be a problem for the actual setup if
        # there is some synchronisation with the CCD camera
        # such that images are taken only after streaming.
        # In this case we have an issue, so we try to fix it.

        # we cannot test def_lock inside buffer_lock as this
        # will lead to a deadlock.

def thread2_func(def_lock, buffer_lock):
    # while True:
    #   with state_lock:
    #       if no_defects:
    #           stream(buffer2)
    #           # Here the streaming is too fast
    #           # compared to the processing on the
    #           # USRP, thus the need for blocking
    #       else:
    #           stream(buffer1)
    #       global no_defects
    #       no_defects = True
    while True:
        global no_defects
        with def_lock:
            if no_defects: # write a non-blocking call
                counter = 1
                for i in range(10000000):
                    counter += 1
                print('No defect exists')
            else:
                counter = 1
                for i in range(10000000):
                    counter += 1
                print('Defect exists')
                global buffer1
                with buffer_lock:
                    buffer1 = 0
                    print("Buffer sent")
            no_defects = True

t1 = threading.Thread(target=thread1_func,args=(server_socket,def_lock,buffer_lock,))
t2 = threading.Thread(target=thread2_func,args=(def_lock,buffer_lock,))

t1.start()
t2.start()


"""
Expt results:

1) If we connect client only after streaming is done

No defect exists
No defect exists
No defect exists
Buffer ready
No defect exists
No defect exists
Defect exists
Buffer sent
No defect exists
No defect exists
Buffer ready
No defect exists
No defect exists
No defect exists
Defect exists
Buffer sent
No defect exists
No defect exists
No defect exists
No defect exists

2) if we connect clients rapidly such that buffer may get replaced

No defect exists
Buffer ready
No defect exists
No defect exists
No defect exists
No defect exists
No defect exists
Buffer ready
Defect exists
Buffer sent
No defect exists
Buffer ready
Defect exists
Buffer sent
No defect exists
Defect exists
Buffer sent
No defect exists
No defect exists
No defect exists
No defect exists
No defect exists
"""