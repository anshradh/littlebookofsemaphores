# %%
from threading import Semaphore, Lock, Thread

# %%
# Want a1 to happen before b2 and b1 to happen before a2 (Rendezvous)
aArrived = Semaphore(0)
bArrived = Semaphore(0)


def threada():
    print(2)
    aArrived.release()
    bArrived.acquire()
    print(5)


def threadb():
    print(3)
    bArrived.release()
    aArrived.acquire()
    print(4)


a = Thread(target=threada)
b = Thread(target=threadb)
a.start()
b.start()
a.join()
b.join()
# %%
# Want to force only one update to count (Mutex)
count = 0
lock = Lock()


def threada():
    global count
    lock.acquire()
    count += 1
    print(count)
    lock.release()


def threadb():
    global count
    lock.acquire()
    count += 1
    print(count)
    lock.release()


a = Thread(target=threada)
b = Thread(target=threadb)
a.start()
b.start()
# %%
# Want to force only multiple threads to update count (Multiplex)
count = 0
multiplex = Semaphore(4)


def thread_i():
    global count
    multiplex.acquire()
    count += 1
    print(count)
    multiplex.release()


threads = []
for i in range(8):
    t = Thread(target=thread_i)
    threads.append(t)
    t.start()
for t in threads:
    t.join()

# %%
# Generalize Rendevous to multiple threads (Barrier)
count = 0
mutex = Lock()
barrier = Semaphore(0)


def thread_i(n):
    global count
    mutex.acquire()
    count += 1
    mutex.release()
    if count == n:
        barrier.release()
    barrier.acquire()
    print(count)
    barrier.release()


# n = 5
threads = []
for i in range(5):
    t = Thread(target=thread_i, args=(5,))
    threads.append(t)
    t.start()
for t in threads:
    t.join()
# %%
# Make Barrier reusable
count = 0
mutex = Lock()
barrier1 = Semaphore(0)
barrier2 = Semaphore(1)


def thread_f(n):
    global count
    mutex.acquire()
    count += 1
    if count == n:
        barrier2.acquire()
        barrier1.release()
    mutex.release()
    barrier1.acquire()
    barrier1.release()
    print("Critical section")
    mutex.acquire()
    count -= 1
    if count == 0:
        barrier1.acquire()
        barrier2.release()
    mutex.release()
    barrier2.acquire()
    barrier2.release()


for i in range(3):
    threads = []
    for _ in range(5):
        t = Thread(target=thread_f, args=(5,))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
# %%
class Barrier:
    def __init__(self, n):
        self.n = n
        self.count = count
        self.mutex = Lock()
        self.t1 = Semaphore(0)
        self.t2 = Semaphore(1)

    def phase1(self):
        self.mutex.acquire()
        self.count += 1
        if self.count == self.n:
            for _ in range(self.n):
                self.t1.release()
        self.mutex.release()
        self.t1.acquire()

    def phase2(self):
        self.mutex.acquire()
        self.count -= 1
        if self.count == 0:
            for _ in range(self.n):
                self.t2.release()
        self.mutex.release()
        self.t2.acquire()

    def wait(self):
        self.phase1()
        self.phase2()


# %%
barrier = Barrier(5)


def thread_f():
    barrier.phase1()
    print("Critical Section")
    barrier.phase2()


for i in range(3):
    threads = []
    for _ in range(5):
        t = Thread(target=thread_f)
        t.start()
        threads.append(t)
    for t in threads:
        t.join()


# %%
# Queue
leader_queue = Semaphore(0)
follower_queue = Semaphore(0)


def leaderThread():
    follower_queue.release()
    leader_queue.acquire()
    print("Leader paired")


def followerThread():
    follower_queue.acquire()
    leader_queue.release()
    print("Follower paired")


for i in range(5):
    leader = Thread(target=leaderThread)
    follower = Thread(target=followerThread)
    leader.start()
    follower.start()
    leader.join()
    follower.join()

# %%
# Exclusive paired
mutex = Lock()
follower_count = 0
leader_count = 0
follower_queue = Semaphore(0)
leader_queue = Semaphore(0)
rendezvous = Semaphore(0)


def follower_thread():
    global follower_count, leader_count
    mutex.acquire()
    if leader_count > 0:
        leader_count -= 1
        leader_queue.release()
    else:
        follower_count += 1
        mutex.release()
        follower_queue.acquire()

    print("Follower Dancing")
    rendezvous.acquire()
    mutex.release()


def leader_thread():
    global follower_count, leader_count
    mutex.acquire()
    if follower_count > 0:
        follower_count -= 1
        follower_queue.release()
    else:
        leader_count += 1
        mutex.release()
        leader_queue.acquire()

    print("Leader Dancing")
    rendezvous.release()


threads = []
for _ in range(5):
    leader = Thread(target=leader_thread)
    follower = Thread(target=follower_thread)
    leader.start()
    follower.start()
    leader.join()
    follower.join()


# %%
