# %%
import threading

count = 0
counts_list = []


def f():
    for i in range(100):
        global count
        temp = count
        count = temp + 1
    global counts_list
    counts_list.append(count)


threads = []
for i in range(100):
    t = threading.Thread(target=f)
    threads.append(t)
    t.start()
ret = []
for t in threads:
    t.join()
print(counts_list)
# %%
