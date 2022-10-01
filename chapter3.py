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


def thread_i(n):
    global count

    mutex.acquire()
    count += 1
    if count == n:
        barrier2.acquire()
        barrier1.release()
    mutex.release()
    barrier1.acquire()
    barrier1.release()

    print(count)

    mutex.acquire()
    count -= 1
    if count == 0:
        barrier1.acquire()
        barrier2.release()
    mutex.release()
    barrier2.acquire()
    barrier2.release()


# n = 5
for l in range(2):
    threads = []
    for i in range(5):
        t = Thread(target=thread_i, args=(5,))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()

# %%
# Queue
leaderQueue = Semaphore(0)
followerQueue = Semaphore(0)


def leaderThread():
    followerQueue.release()
    leaderQueue.acquire()
    print("Leader paired")


def followerThread():
    followerQueue.acquire()
    leaderQueue.release()
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
leaderQueue = Semaphore(0)
followerQueue = Semaphore(0)
mutex = Lock()
leaderCount = 0
followerCount = 0
rendezvous = Semaphore(0)


def leaderThread():
    global followerCount
    global leaderCount
    mutex.acquire()
    if followerCount > 0:
        followerCount -= 1
        followerQueue.release()
    else:
        leaderCount += 1
        mutex.release()
        leaderQueue.acquire()
    print("Leader paired")
    rendezvous.acquire()
    mutex.release()


def followerThread():
    global followerCount
    global leaderCount
    mutex.acquire()
    if leaderCount > 0:
        leaderCount -= 1
        leaderQueue.release()
    else:
        followerCount += 1
        mutex.release()
        followerQueue.acquire()
    print("Follower paired")
    rendezvous.release()


for i in range(5):
    leader = Thread(target=leaderThread)
    follower = Thread(target=followerThread)
    leader.start()
    follower.start()
    leader.join()
    follower.join()

# %%
