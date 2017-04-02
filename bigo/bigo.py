from timeit import Timer
from random import randint


def t1():
    global l1, k
    return l1[k]


def t2():
    global l1, k
    return len(set(l1))


def kth_smallest():
    global l1, k
    return list(set(l1))[k]

tt1 = Timer('t1()', 'from __main__ import t1, l1, k')
tt2 = Timer('t2()', 'from __main__ import t2, l1, k')
ktime = Timer('kth_smallest()', 'from __main__ import kth_smallest, l1, k')
for i in range(100, 1000, 10):
    l1 = [randint(0, 100) for i in range(0, i)]
    k = randint(0, 10)
    pt1 = tt1.timeit(number=100)
    pt2 = tt2.timeit(number=100)
    pt3 = ktime.timeit(number=100)
    print("%15.5f\t%15.5f\t%15.5f" % (pt1, pt2, pt3))
