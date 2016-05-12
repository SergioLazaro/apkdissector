import os

from collector.pscoutDB import PScoutDB
from collector.pscoutDB import Permission

__author__ = 'sergio'

class Reader:

    def __init__(self,path, dbpath):
        self.path = path    #Path JSON File with enforcements
        self.fd = None
        self.db = None
        self.dbpath = dbpath
        self.start()

    def start(self):    #Working method
        self.checkFixNeeded()

    '''
        Check if the last character is a ','. If it is a ',' the json file is not well ended
        and it should be fixed.
    '''
    def checkFixNeeded(self):
        self._open('rb+')
        self.fd.seek(-1,2)
        if self.fd.read() == ',' :
            self._close()
            self.fixNotEnded()
        else:
            print "[*] JSON file well formed. Fixing not needed..."

    '''
        Enforcement JSON files end with a ','. Its necessary to delete it and add ']}'
    '''
    def fixNotEnded(self):
        print "[*] Fixing the file to a well formed JSON..."
        self._open('a')  #Getting file descriptor
        size = self.fd.tell() #Get size
        self.fd.truncate(size-1)
        self.fd.seek(0,2)  #2 = SEEK_END
        self._write("}]}")
        self._close()

    def checkPermissionInfo(self,permission):
        self._open('r')
        self.db = PScoutDB(None,self.dbpath)
        array = self.db.querypermission(permission)

        #Check interesting permission methods
        self.lookForInterestingMethods(array)

    def lookForInterestingMethods(self,array):

        for permission in array:
            print "foo"

    def _open(self,mode):
        self.fd = open(self.path, mode)
        #print "OPEN SIZE: " + str(self.fd.tell())

    def _write(self,message):
        self.fd.write(message)

    def _close(self):
        self.fd.close()
