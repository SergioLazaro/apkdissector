__author__ = 'sergio'

import threading, time, random, datetime

class ThreadManager:

    def __init__(self):
        print "hello"


class Worker(threading.Thread):

    def __init__(self, id, t):
        threading.Thread.__init__(self)
        self.id = id
        self.t = t

    def run(self):
        global working
        print "Worker " + str(self.id) + " go to sleep " + str(self.t) + " seconds."
        time.sleep(self.t)
        print "Worker " + str(self.id) + " finished"
        if lock.locked():
            print "Thread " + str(self.id) + " RELEASE"
            lock.release()
            working -= 1


def launchThread(i,lock):
    waittime = random.randint(5,8)
    t = Worker(i,waittime)
    t.start()

#tm = ThreadManager()
global lock, working
lock = threading.Lock()
i = 0
working = 0
for i in range(5):      #we launch 5 tasks but can be run just 3
    if working < 3:
        print "Launching thread number " + str(i)
        launchThread(i,lock)
    else:
        lock.acquire()
        print "Thread " + str(i) + " waiting until release..."
        launchThread(i,lock)
    working += 1

