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
        task = self.tasks.get()
        task.start()
        print "Worker task finished!!"
        self.tasks.task_done()
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
