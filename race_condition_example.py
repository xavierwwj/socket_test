import threading
import time
import concurrent.futures

"""
A race condition or race hazard is the condition of an electronics, software, or other system 
where the system's substantive behavior is dependent on the sequence or timing of other uncontrollable events.

It is safe if the multiple threads just want to read the state but not when the threads need to modify the state
and the order of modification matters.
"""
threads = []
global_state = 1

def thread_func(thread_no):
    # The first print is not blocked and run first, while the next thread is made,
    # so the first print are always in sequence
    print(str(1+thread_no)+" start")

    time.sleep(2)
    # Here is when we have a blocking call on all threads.
    # Since all threads have blocked, and are released around the same time, there is some uncertainty.
    # As a result, there is race condition that results in undefined behaviour. Running repeatedly
    # gives different sequence of events as result. 

    # time.sleep(thread_no*0.001)
    # If we add a clear blocking time order, then there will no longer be the race condition
    # It appears that any smaller than this power of -3, the uncertainty still remains.

    print(str(1+thread_no)+" end")
    global global_state
    global_state = global_state*(1+thread_no)+(thread_no+1)
    print(global_state)
    # Create an operation that does not commute for all three thread numbers
    # to clearly show that the race condition leads to different results when
    # modifying a variable.
    

with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
    executor.map(thread_func, range(3))
    # Here, this mapping creates threads one at a time

print(global_state)


"""
One of the result is this:
    1 start
    2 start
    3 start
    1 end
    2
    3 end2 end
    6

    21
    21

Another is this:
    1 start
    2 start
    3 start
    2 end3 end1 end
    2


    6
    21
    21

Another is this:
    1 start
    2 start
    3 start
    1 end2 end
    4
    3 end
    15

    16
    16

This suggests that without blocking, some threads may process when the other threads are not done.
"""