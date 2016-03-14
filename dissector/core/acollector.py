__author__ = 'vaioco'

class Acollector:
    def __init__(self, t):
        print 'running %s on %s... ' % (self.__class__ , t.get_name())
        self.target = t
        self.run()

    def run(self):
        pass
