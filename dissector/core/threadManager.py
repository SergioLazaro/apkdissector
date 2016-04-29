__author__ = 'sergio'

import threading, time, random, datetime

class ThreadManager:

    def __init__(self,limit):
        self.limit = limit
        self.lock = threading.Lock()
        self.working = 0

    def manage(self,t):
        if self.working < self.limit:
            print "Launching thread number " + str(i)
            t.start()
            self.working += 1
        else:
            self.lock.acquire()
            print "Thread " + str(i) + " waiting until release..."
            t.start()
            self.working += 1

class Worker(threading.Thread):

    def __init__(self, id, t, lock, working):
        threading.Thread.__init__(self)
        self.id = id
        self.t = t
        self.lock = lock
        self.working = working

    def run(self):
        print "Worker " + str(self.id) + " go to sleep " + str(self.t) + " seconds."
        time.sleep(self.t)
        print "Worker " + str(self.id) + " finished"
        if self.lock.locked():
            print "Thread " + str(self.id) + " RELEASE"
            try:
                self.lock.release()
            except:
                print "Lock unlocked."
            self.working -= 1
'''
start = time.time()
tm = ThreadManager(2)
for i in range(5):      #we launch 5 tasks but can be run just 3
    print "WORKING : " + str(tm.working) + " LOCK STATE: " + str(tm.lock.locked())
    waittime = random.randint(8,10)
    t = Worker(i,waittime,tm.lock,tm.working)
    tm.manage(t)
    time.sleep(2)
waiting = threading.enumerate()
for thread in waiting[1:]:
    thread.join()
end = time.time()
print "Total time %.2f" % (end - start)
'''


