from core.writers import DeobfuscatorWriter

__author__ = 'vaioco'

from androguard.core.bytecodes.dvm import *

class Deobfuscator:
    def __init__(self,target):
        self.target = target
        self.analyze()

    def analyze(self):
        self.itemlist = []
        self.myclassedefitem = self.target.get_classes()
        print "there are %s classes into the target APK" % (len(self.myclassedefitem))
        for c in self.myclassedefitem:
            #print 'classname: ' + c.get_name()
            fields = c.get_fields()
            for f in fields:
                flags =  f.get_access_flags()
                #f.show()
                if ((0x8 & flags) == 0x8):
                    if "[B" in f.get_descriptor() or "Ljava/lang/String;" in f.get_descriptor():
                        print f.get_name() + ': ' + f.get_descriptor()
                        self.itemlist.append(f)
        for s in self.itemlist:
            DeobfuscatorWriter.write("provami.deobf",s.get_class_name() + s.get_name() )