"""
For daemon threads, they do not stop the interpreted from exiting. During the exit process, the main thread and its children will
be killed.

Daemon threads are useful for data logging or garbage collecting etc, processes that you want to run throughout, and where you
don't want to care about having to kill them, so you can just set an infinite loop and let the thread die when the main thread ends
"""

import threading
import time

def test_func(thread_no):
    counter = 1
    while True:
        print("thread_no " + str(thread_no) + ": " + str(counter))
        counter += 1
        time.sleep(1)

thread1 = threading.Thread(target = test_func, args = (1,), daemon = True)
thread2 = threading.Thread(target = test_func, args = (2,))

thread1.start()
thread2.start()
    # In the case that this thread is also running, we will get a total of 3 threads (seen in Activity Monitory)
    # Additionally, at the end of 10 seconds after the main thread finishes sleeping, the program will try to
    # join thread2, which never finishes. thread1 then also continues concurrently (due to the one second block in
    # both threads). 

time.sleep(10) 
print("Program ending")
# Block main thread for 10 seconds, the child thread should be running
# After this, the program ends and the child thread is killed also despite incompletion

#thread1.join() # If we called this, then we force the daemon thread to also join. This causes the infinite loop as well.

