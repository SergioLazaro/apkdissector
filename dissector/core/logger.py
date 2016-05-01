__author__ = 'sergio'

class Logger:

    def __init__(self,filepath):
        self.filepath = filepath
        self.open()

    def open(self):
        #File descriptor for the log file
        self.fd = open(self.filepath,'w')

    def close(self):
        self.fd.close()

    def write(self,line):
        self.fd.write(line)

