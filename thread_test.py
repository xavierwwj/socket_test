import threading

def thread_func1():
    while True:
        print('1')

def thread_func2():
    while True:
        print('2')

t1 = threading.Thread(target=thread_func1)
t2 = threading.Thread(target=thread_func2)

t1.start()
t2.start()

# This experiment will show that once awhile the priority switches. We get a string of 1s, then string of 2s, then rotate randomly