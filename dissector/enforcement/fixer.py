__author__ = 'sergio'

class Fixer:

    def __init__(self,path):
        self.path = path    #Path JSON File with enforcements
        self.fd = None
        self.start()

    def start(self):    #Working method
        self._open('r')
        self.checkFixNeeded()

    '''
        Check if the last character is a ','. If it is a ',' the json file is not well ended
        and it should be fixed.
    '''
    def checkFixNeeded(self):
        self._open('rb+')
        self.fd.seek(-1,2)
        r = self.fd.read()
        r.rstrip()
        if self.fd.read() == ',':
            self._close()
            self.fixNotEnded(1)
        elif self.fd.read() == '':
            self._close()
            self.fixNotEnded(2)
        else:
            print "[*] JSON file well formed. Fixing not needed..."

    '''
        Enforcement JSON files end with a ','. Its necessary to delete it and add ']}'
    '''
    def fixNotEnded(self,position):
        print "[*] Fixing the file to a well formed JSON..."
        self._open('a')  #Getting file descriptor
        size = self.fd.tell() #Get size
        self.fd.truncate(size - position)
        self.fd.seek(0,2)  #2 = SEEK_END
        self._write("]}")
        self._close()

    def _open(self,mode):
        self.fd = open(self.path, mode)
        #print "OPEN SIZE: " + str(self.fd.tell())

    def _write(self,message):
        self.fd.write(message)

    def _close(self):
        self.fd.close()
