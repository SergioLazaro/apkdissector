__author__ = 'sergio'

import threading, time, random, datetime
from Queue import Queue

class ThreadManager:
    def __init__(self,num_threads):
        self.lock = threading.Lock()
        self.num_threads = num_threads
        self.tasks = Queue(num_threads)
    def add_task(self, tasks_list):
        for t in tasks_list:
            self.tasks.put(t)
            Worker(self.tasks).start()
    def wait_completition(self):
        self.tasks.join()
    def areTaskRunning(self):
        print self.tasks.empty()

class Worker(threading.Thread):
    def __init__(self, tasks):
        threading.Thread.__init__(self)
        self.tasks = tasks
    def run(self):
        task = self.tasks.get()
        task.start()
        self.tasks.task_done()
