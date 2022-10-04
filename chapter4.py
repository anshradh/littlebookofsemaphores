# %%
from threading import Semaphore, Lock, Thread, local, Barrier
from queue import Queue, SimpleQueue, PriorityQueue
from time import sleep
from collections import deque
import random

# %%
# Producer-consumer
def waitForEvent(i):
    print(f"Waiting for event {i}")
    sleep(random.uniform(0, 3))
    event = lambda: random.uniform(0, 1)
    print(f"Event {i}")
    return event


buffer = deque([])
buffer_gate = Semaphore(0)
buffer_lock = Lock()


def producer_thread(i):
    event = waitForEvent(i)
    buffer_lock.acquire()
    buffer.append(event)
    buffer_lock.release()
    buffer_gate.release()


def consumer_thread():
    buffer_gate.acquire()
    buffer_lock.acquire()
    event = buffer.popleft()
    buffer_lock.release()
    event()


threads = []
for i in range(5):
    p_thread = Thread(target=producer_thread, args=(i,))
    c_thread = Thread(target=consumer_thread)
    p_thread.start()
    c_thread.start()
    threads.append((p_thread, c_thread))

for t in threads:
    t[0].join()
    t[1].join()

# %%
# Produce-consumer with finite buffer
def waitForEvent(i):
    print(f"Waiting for event {i}")
    sleep(random.uniform(0, 4))
    event = lambda: random.uniform(0, 1)
    print(f"Event {i}")
    return event


buffer_size = 2
buffer_size_sem = Semaphore(buffer_size)
buffer = deque([])
buffer_gate = Semaphore(0)
buffer_lock = Lock()


def producer_thread(i):
    event = waitForEvent(i)
    buffer_size_sem.acquire()
    buffer_lock.acquire()
    buffer.append(event)
    buffer_lock.release()
    buffer_gate.release()


def consumer_thread():
    buffer_gate.acquire()
    buffer_lock.acquire()
    event = buffer.popleft()
    buffer_lock.release()
    buffer_size_sem.release()
    event()


threads = []
for i in range(5):
    p_thread = Thread(target=producer_thread, args=(i,))
    c_thread = Thread(target=consumer_thread)
    p_thread.start()
    c_thread.start()
    threads.append((p_thread, c_thread))

for t in threads:
    t[0].join()
    t[1].join()
# %%
# Readers-writers

data = dict()
empty = Lock()
reader_count = 0
mutex = Lock()


def writer_thread(key, val):
    empty.acquire()
    data[key] = val
    empty.release()


def reader_thread(key):
    global reader_count
    mutex.acquire()
    reader_count += 1
    if reader_count == 1:
        empty.acquire()
    mutex.release()
    sleep(random.uniform(1, 3))
    print(data[key])
    mutex.acquire()
    reader_count -= 1
    if reader_count == 0:
        empty.release()
    mutex.release()


readers = []
for r in range(5):
    r_t = Thread(target=reader_thread, args=(r % 3,))
    readers.append(r_t)

writers = []
for w in range(3):
    w_t = Thread(target=writer_thread, args=(w, w * 2))
    writers.append(w_t)

for w in writers:
    w.start()
    w.join()

for r in readers:
    r.start()
    r.join()

# %%
class Lightswitch:
    def __init__(self):
        self.count = 0
        self.mutex = Lock()

    def lock(self, semaphore):
        self.mutex.acquire()
        self.count += 1
        if self.count == 1:
            semaphore.acquire()
        self.mutex.release()

    def unlock(self, semaphore):
        self.mutex.acquire()
        self.count -= 1
        if self.count == 0:
            semaphore.release()
        self.mutex.release()


# %%
data = dict()
empty = Lock()
lightswitch = Lightswitch()


def writer_thread(key, val):
    empty.acquire()
    data[key] = val
    empty.release()


def reader_thread(key):
    lightswitch.lock(empty)
    sleep(random.uniform(1, 3))
    print(data[key])
    lightswitch.unlock(empty)


readers = []
for r in range(5):
    r_t = Thread(target=reader_thread, args=(r % 3,))
    readers.append(r_t)

writers = []
for w in range(3):
    w_t = Thread(target=writer_thread, args=(w, w * 2))
    writers.append(w_t)

for w in writers:
    w.start()
    w.join()

for r in readers:
    r.start()
    r.join()
# %%
# no-starve readers and writers
data = dict()
empty = Lock()
lightswitch = Lightswitch()
turnstile = Semaphore(1)


def writer_thread(key, val):
    turnstile.acquire()
    empty.acquire()
    data[key] = val
    turnstile.release()
    empty.release()


def reader_thread(key):
    turnstile.acquire()
    turnstile.release()
    lightswitch.lock(empty)
    sleep(random.uniform(1, 2))
    print(data[key])
    lightswitch.unlock(empty)


readers = []
for r in range(5):
    r_t = Thread(target=reader_thread, args=(r % 3,))
    readers.append(r_t)

writers = []
for w in range(3):
    w_t = Thread(target=writer_thread, args=(w, w * 2))
    writers.append(w_t)

for w in writers:
    w.start()
    w.join()

for r in readers:
    r.start()
    r.join()

# %%
# priority to writers



def writer_thread(key, val):



def reader_thread(key):



readers = []
for r in range(5):
    r_t = Thread(target=reader_thread, args=(r % 3,))
    readers.append(r_t)

writers = []
for w in range(3):
    w_t = Thread(target=writer_thread, args=(w, w * 2))
    writers.append(w_t)

for w in writers:
    w.start()
    w.join()

for r in readers:
    r.start()
    r.join()
