__author__ = 'sergio'

import threading, time, random, datetime
from Queue import Queue

class ThreadManager:
    def __init__(self,num_threads):
        self.lock = threading.Lock()
        self.num_threads = num_threads
        self.tasks = Queue(num_threads)
        #for _ in range(self.num_threads): Worker(self.tasks)
    def add_task(self, tasks_list):
        for t in tasks_list:
            self.tasks.put(t)
            Worker(self.tasks).start()
        print "Queue len: " + str(self.tasks.qsize())
    def wait_completition(self):
        self.tasks.join()
        print "Thread Manager: tasks completed!"
    def areTaskRunning(self):
        print self.tasks.empty()

class Worker(threading.Thread):
    def __init__(self, tasks):
        threading.Thread.__init__(self)
        self.tasks = tasks
    def run(self):
<<<<<<< HEAD
        task = self.tasks.get()
        task.start()
        print "Worker task finished!!"
        self.tasks.task_done()
=======
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
>>>>>>> 020840b949167fbf6c50c2b8fcd58ffb618fa135
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

'''
