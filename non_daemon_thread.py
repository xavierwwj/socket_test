"""
- For non-daemon threads, the program will wait till these threads are done at the end of the program before exiting
- Specifically, at the end of the program, there will be a call .join() for the non-daemon alive threads. 
- This is a blocking call that awaits completion of the thread.
    - If you look at the source for Python threading, you’ll see that threading._shutdown() walks through all of the
    running threads and calls .join() on every one that does not have the daemon flag set.
- Experiment:
    - thread1.start(), thread2.start(), end prog
    - thread1.start(), thread1.join(). thread2.start() end prog
    - Compare the two, at the end of the program, join will be called implicitly, so we omit the necessary ones
- Result:
    - Case 1 -> concurrency
    - Case 2 -> One after another

    
"""

import threading
import time

def test_func(thread_no):
    print("thread_no: " + str(thread_no))
    time.sleep(2) 
    # Setting time.sleep will block the thread. This means that the processor will go ahead with the other thread first
    # Removing this will result in the thread reaching completion first.
    print("thread_no " + str(thread_no) + " completed")

thread1 = threading.Thread(target = test_func, args = (1,))
thread2 = threading.Thread(target = test_func, args = (2,))

print("Experiment 1 Start")
thread1.start()
thread2.start()
thread1.join()
thread2.join()
print("Experiment 1 Complete")


thread3 = threading.Thread(target = test_func, args = (3,))
thread4 = threading.Thread(target = test_func, args = (4,))

time.sleep(5)
print("Experiment 2 Start")
thread3.start()
thread3.join()
thread4.start()
thread4.join() # Here we explicitly wait for thread to end then print afterwards
print("Experiment 2 Complete")

